import org.apache.spark.SparkContext._

// 1) Leer todos los logs
val registros = sc.textFile("/app/registros/*.txt")

// 2) Definir eventos clave
val eventosClave = Set(
  "ALERTA_SOBRECALENTAMIENTO",
  "REINICIO_SISTEMA",
  "CALIBRACION_AUTOMATICA",
  "CARGA_EXCESIVA",
  "PAUSA_NO_PROGRAMADA"
)

// 3) Filtra, parsea y mapea a pares (String,Int)
val pares = registros.flatMap { line =>
  val parts = line.split(" - ")
  if (parts.length >= 2 && eventosClave.contains(parts(1)))
    Some((parts(1), 1))
  else
    None
}

// 4) Reduce por clave
val conteos = pares.reduceByKey(_ + _)

// 5) Traer al driver y mostrar
val resultado = conteos.collect()
println("Conteo de eventos:")
resultado.foreach{ case (ev, cnt) =>
  println(f"$ev%-25s $cnt%5d")
}