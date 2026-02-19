#include "wokwi-api.h"
#include <math.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdlib.h>

#define I2C_ADDR 0x57

// Minimal register map needed by SparkFun MAX3010x library
#define REG_INTSTAT1 0x00
#define REG_INTSTAT2 0x01
#define REG_INTEN1 0x02
#define REG_INTEN2 0x03
#define REG_FIFOWRITEPTR 0x04
#define REG_FIFOOVERFLOW 0x05
#define REG_FIFOREADPTR 0x06
#define REG_FIFODATA 0x07
#define REG_FIFOCONFIG 0x08
#define REG_MODECONFIG 0x09
#define REG_PARTICLECFG 0x0A
#define REG_LED1_PA 0x0C
#define REG_LED2_PA 0x0D
#define REG_REVID 0xFE
#define REG_PARTID 0xFF

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

#define FIFO_DEPTH 32

typedef struct {
  i2c_dev_t i2c;
  timer_t timer;

  uint32_t attr_bpm;
  uint32_t attr_finger;

  uint8_t regs[256];
  uint8_t reg_ptr;
  bool expect_reg;

  uint8_t wr;
  uint8_t rd;
  uint8_t byte_idx; // RED[3] + IR[3]

  uint32_t fifo_red[FIFO_DEPTH];
  uint32_t fifo_ir[FIFO_DEPTH];

  float phase;
  uint32_t rng;
  uint32_t sample_rate_hz;
} state_t;

static inline uint32_t lcg(state_t *s) {
  s->rng = s->rng * 1664525u + 1013904223u;
  return s->rng;
}

static inline int32_t noise(state_t *s, int32_t amp) {
  uint32_t r = (lcg(s) >> 8) % (uint32_t)(2 * amp + 1);
  return (int32_t)r - amp;
}

static inline uint32_t clamp18(int32_t v) {
  if (v < 0) {
    v = 0;
  }
  if (v > 0x3FFFF) {
    v = 0x3FFFF;
  }
  return (uint32_t)v;
}

static uint16_t decode_sample_rate(uint8_t spo2_cfg) {
  uint8_t sr = (spo2_cfg >> 2) & 0x07;
  switch (sr) {
    case 0:
      return 50;
    case 1:
      return 100;
    case 2:
      return 200;
    case 3:
      return 400;
    case 4:
      return 800;
    case 5:
      return 1000;
    case 6:
      return 1600;
    case 7:
      return 3200;
    default:
      return 100;
  }
}

static void fifo_clear(state_t *s) {
  s->wr = 0;
  s->rd = 0;
  s->byte_idx = 0;
  s->regs[REG_FIFOWRITEPTR] = 0;
  s->regs[REG_FIFOREADPTR] = 0;
  s->regs[REG_FIFOOVERFLOW] = 0;
}

static void update_timer(state_t *s) {
  uint16_t sr = decode_sample_rate(s->regs[REG_PARTICLECFG]);
  if (sr == 0) {
    sr = 100;
  }
  s->sample_rate_hz = sr;

  uint32_t period_us = 1000000u / (uint32_t)sr;
  if (period_us < 500) {
    period_us = 500;
  }
  timer_start(s->timer, period_us, true);
}

static void reset_device(state_t *s) {
  uint8_t part = s->regs[REG_PARTID];
  uint8_t rev = s->regs[REG_REVID];

  for (int i = 0; i < 256; i++) {
    s->regs[i] = 0;
  }

  s->regs[REG_PARTID] = part;
  s->regs[REG_REVID] = rev;
  s->regs[REG_FIFOCONFIG] = 0x10;
  s->regs[REG_MODECONFIG] = 0x03;
  s->regs[REG_PARTICLECFG] = 0x04; // 100 Hz default
  s->regs[REG_LED1_PA] = 0x1F;
  s->regs[REG_LED2_PA] = 0x1F;

  fifo_clear(s);
  update_timer(s);
}

static void fifo_push(state_t *s, uint32_t red18, uint32_t ir18) {
  uint8_t next = (uint8_t)((s->wr + 1) & 0x1F);
  if (next == s->rd) {
    s->rd = (uint8_t)((s->rd + 1) & 0x1F);
    s->regs[REG_FIFOREADPTR] = s->rd;
  }

  s->fifo_red[s->wr] = red18 & 0x3FFFF;
  s->fifo_ir[s->wr] = ir18 & 0x3FFFF;
  s->wr = next;
  s->regs[REG_FIFOWRITEPTR] = s->wr;
  s->regs[REG_INTSTAT1] |= 0x40; // PPG_RDY
}

static uint8_t fifo_read_byte(state_t *s) {
  if (s->wr == s->rd) {
    return 0;
  }

  uint32_t red = s->fifo_red[s->rd];
  uint32_t ir = s->fifo_ir[s->rd];
  uint8_t out = 0;

  switch (s->byte_idx) {
    case 0:
      out = (uint8_t)((red >> 16) & 0x03);
      break;
    case 1:
      out = (uint8_t)((red >> 8) & 0xFF);
      break;
    case 2:
      out = (uint8_t)(red & 0xFF);
      break;
    case 3:
      out = (uint8_t)((ir >> 16) & 0x03);
      break;
    case 4:
      out = (uint8_t)((ir >> 8) & 0xFF);
      break;
    case 5:
      out = (uint8_t)(ir & 0xFF);
      break;
    default:
      out = 0;
      break;
  }

  s->byte_idx++;
  if (s->byte_idx >= 6) {
    s->byte_idx = 0;
    s->rd = (uint8_t)((s->rd + 1) & 0x1F);
    s->regs[REG_FIFOREADPTR] = s->rd;
    if (s->wr == s->rd) {
      s->regs[REG_INTSTAT1] &= (uint8_t)~0x40;
    }
  }

  return out;
}

static bool on_connect(void *user_data, uint32_t address, bool read) {
  (void)address;
  state_t *s = (state_t *)user_data;
  if (!read) {
    s->expect_reg = true;
  }
  return true;
}

static bool on_write(void *user_data, uint8_t data) {
  state_t *s = (state_t *)user_data;

  if (s->expect_reg) {
    s->reg_ptr = data;
    s->expect_reg = false;
    return true;
  }

  uint8_t reg = s->reg_ptr;
  s->regs[reg] = data;

  if (reg == REG_MODECONFIG) {
    if (data & 0x40) {
      reset_device(s);
      s->regs[REG_MODECONFIG] &= (uint8_t)~0x40;
    }
  } else if (reg == REG_PARTICLECFG) {
    update_timer(s);
  } else if (reg == REG_FIFOWRITEPTR) {
    s->wr = data & 0x1F;
    s->regs[REG_FIFOWRITEPTR] = s->wr;
  } else if (reg == REG_FIFOREADPTR) {
    s->rd = data & 0x1F;
    s->regs[REG_FIFOREADPTR] = s->rd;
    s->byte_idx = 0;
  }

  s->reg_ptr++;
  return true;
}

static uint8_t on_read(void *user_data) {
  state_t *s = (state_t *)user_data;

  if (s->reg_ptr == REG_FIFODATA) {
    return fifo_read_byte(s);
  }

  uint8_t reg = s->reg_ptr;
  uint8_t value = s->regs[reg];

  if (reg == REG_INTSTAT1 || reg == REG_INTSTAT2) {
    s->regs[reg] = 0;
  }

  s->reg_ptr++;
  return value;
}

static void on_timer(void *user_data) {
  state_t *s = (state_t *)user_data;

  if (s->regs[REG_MODECONFIG] & 0x80) {
    return;
  }

  uint32_t bpm = attr_read(s->attr_bpm);
  if (bpm < 30) {
    bpm = 30;
  }
  if (bpm > 220) {
    bpm = 220;
  }

  bool finger = attr_read(s->attr_finger) != 0;
  float sr = (float)(s->sample_rate_hz ? s->sample_rate_hz : 100);
  float bps = (float)bpm / 60.0f;

  s->phase += (2.0f * (float)M_PI) * (bps / sr);
  if (s->phase >= (2.0f * (float)M_PI)) {
    s->phase -= (2.0f * (float)M_PI);
  }

  float t = s->phase;
  float sigma1 = 0.14f;
  float sigma2 = 0.30f;
  float p1 = expf(-0.5f * (t / sigma1) * (t / sigma1));
  float p2 = 0.22f * expf(-0.5f * ((t - 0.85f) / sigma2) * ((t - 0.85f) / sigma2));

  int32_t base_ir = finger ? 90000 : 10000;
  int32_t base_red = finger ? 75000 : 9000;
  int32_t amp_ir = finger ? 32000 : 400;
  int32_t amp_red = finger ? 22000 : 300;
  int32_t noise_amp = finger ? 180 : 35;

  int32_t ir = base_ir + (int32_t)(amp_ir * (p1 + p2)) + noise(s, noise_amp);
  int32_t red = base_red + (int32_t)(amp_red * (p1 + p2)) + noise(s, noise_amp);

  fifo_push(s, clamp18(red), clamp18(ir));
}

void chip_init(void) {
  state_t *s = (state_t *)calloc(1, sizeof(state_t));
  s->rng = 0xC001CAFE;

  s->attr_bpm = attr_init("bpm", 75);
  s->attr_finger = attr_init("finger", 1);

  s->regs[REG_PARTID] = 0x15;
  s->regs[REG_REVID] = 0x00;

  const i2c_config_t i2c_cfg = {
    .address = I2C_ADDR,
    .scl = pin_init("SCL", INPUT_PULLUP),
    .sda = pin_init("SDA", INPUT_PULLUP),
    .connect = on_connect,
    .write = on_write,
    .read = on_read,
    .disconnect = NULL,
    .user_data = s,
  };
  s->i2c = i2c_init(&i2c_cfg);

  const timer_config_t timer_cfg = {
    .callback = on_timer,
    .user_data = s,
  };
  s->timer = timer_init(&timer_cfg);

  reset_device(s);
}
