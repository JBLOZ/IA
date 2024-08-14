import java.io.*;
import java.util.zip.*;

public class ZipUtils {

    public static void zipDirectory(File dir, File zipFile) throws IOException {
        try (FileOutputStream fos = new FileOutputStream(zipFile);
             ZipOutputStream zos = new ZipOutputStream(fos)) {
            zipDirectoryHelper(dir, dir, zos);
        }
    }

    private static void zipDirectoryHelper(File rootDir, File sourceDir, ZipOutputStream zos) throws IOException {
        File[] files = sourceDir.listFiles();
        for (File file : files) {
            if (file.isDirectory()) {
                zipDirectoryHelper(rootDir, file, zos);
            } else {
                try (FileInputStream fis = new FileInputStream(file)) {
                    String zipEntryName = rootDir.toPath().relativize(file.toPath()).toString();
                    zos.putNextEntry(new ZipEntry(zipEntryName));
                    byte[] buffer = new byte[1024];
                    int length;
                    while ((length = fis.read(buffer)) > 0) {
                        zos.write(buffer, 0, length);
                    }
                    zos.closeEntry();
                }
            }
        }
    }
}
