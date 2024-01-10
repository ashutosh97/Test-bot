import software.amazon.awssdk.auth.credentials.EnvironmentVariableCredentialsProvider;
import software.amazon.awssdk.core.ResponseInputStream;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.*;

import java.io.*;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

public class S3ZipFileProcessor {

    public static void main(String[] args) {
        // Source and destination S3 bucket and file paths
        String sourceBucket = "source-bucket";
        String sourceKey = "path/to/source/yourfile.zip";
        String destinationBucket = "destination-bucket";
        String destinationKeyPrefix = "path/to/destination/";

        // Initialize S3 client
        S3Client s3Client = S3Client.builder()
                .region(Region.US_EAST_1) // Replace with your desired region
                .credentialsProvider(EnvironmentVariableCredentialsProvider.create())
                .build();

        // Download the zip file from the source bucket
        downloadAndUnzip(s3Client, sourceBucket, sourceKey, destinationBucket, destinationKeyPrefix);

        // Close the S3 client
        s3Client.close();
    }

    private static void downloadAndUnzip(S3Client s3Client, String sourceBucket, String sourceKey, String destinationBucket, String destinationKeyPrefix) {
        try {
            // Create a GetObjectRequest for the source zip file
            GetObjectRequest getObjectRequest = GetObjectRequest.builder()
                    .bucket(sourceBucket)
                    .key(sourceKey)
                    .build();

            // Get the S3Object
            S3Object s3Object = s3Client.getObject(getObjectRequest);

            // Get the response input stream
            try (ResponseInputStream<GetObjectResponse> objectResponseInputStream = s3Object.read()) {
                // Unzip the file and upload contents to the destination bucket
                unzipAndUpload(s3Client, objectResponseInputStream, destinationBucket, destinationKeyPrefix);
            }

            System.out.println("Zip file processed successfully.");
        } catch (IOException | S3Exception e) {
            System.err.println("Error processing zip file from S3: " + e.getMessage());
        }
    }

    private static void unzipAndUpload(S3Client s3Client, InputStream inputStream, String destinationBucket, String destinationKeyPrefix) throws IOException {
        try (ZipInputStream zipInputStream = new ZipInputStream(inputStream)) {
            ZipEntry zipEntry = zipInputStream.getNextEntry();
            while (zipEntry != null) {
                String entryName = zipEntry.getName();
                String destinationKey = destinationKeyPrefix + entryName;

                // Create a PutObjectRequest for each entry in the zip file
                PutObjectRequest putObjectRequest = PutObjectRequest.builder()
                        .bucket(destinationBucket)
                        .key(destinationKey)
                        .build();

                // Upload the entry to the destination bucket
                s3Client.putObject(putObjectRequest, RequestBody.fromInputStream(zipInputStream, zipEntry.getSize()));

                zipEntry = zipInputStream.getNextEntry();
            }
        }
    }
}
