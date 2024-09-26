import java.io.*;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Timer;
import java.util.TimerTask;

public class BackupManager {

    private static final String MINECRAFT_DIR = "D:\\Desktop\\Server";
    private static final String WORLD_NAME = "world";
    private static final String BACKUP_DIR = "D:\\Desktop\\Server\\worldBackups";

    public static void main(String[] args) {
        // Schedule periodic backups every 15 minutes
        Timer timer = new Timer();
        timer.schedule(new BackupTask(), 0, 15 * 60 * 1000);

        // Add shutdown hook to perform final backup on server stop
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            System.out.println("Stopping Minecraft server...");
            performBackup();
            System.out.println("Server stopped and backup completed.");
        }));

        // Keep the program running
        while (true) {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    private static void performBackup() {
        String timestamp = new SimpleDateFormat("yyyy-MM-dd_HH-mm-ss").format(new Date());
        String backupName = WORLD_NAME + "_backup_" + timestamp + ".zip";
        String backupPath = BACKUP_DIR + "\\" + backupName;

        try {
            System.out.println("Creating backup: " + backupName);
            executeCommand("save-off");
            executeCommand("save-all");
            Thread.sleep(10000);  // Wait for save-all to complete

            File backupDir = new File(BACKUP_DIR);
            if (!backupDir.exists()) {
                backupDir.mkdirs();
            }

            File worldDir = new File(MINECRAFT_DIR, WORLD_NAME);
            ZipUtils.zipDirectory(worldDir, new File(backupPath));

            executeCommand("save-on");
            System.out.println("Backup " + backupName + " created successfully.");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static void executeCommand(String command) throws IOException {
        String fullCommand = "cmd /c echo " + command + " > " + MINECRAFT_DIR + "\\minecraft_input.txt";
        Runtime.getRuntime().exec(fullCommand);
    }

    static class BackupTask extends TimerTask {
        @Override
        public void run() {
            performBackup();
        }
    }
}
