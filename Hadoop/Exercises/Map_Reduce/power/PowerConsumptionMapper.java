package com.example.hadoop;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

public class PowerConsumptionMapper extends Mapper<LongWritable, Text, IntWritable, DateConsumptionWritable> {
    private IntWritable householdID = new IntWritable();
    private boolean isHeader = true; // Skip the header row

    @Override
    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        if (isHeader) { // If this is the first row
            isHeader = false; // Set to false after the first row
            return;
        }

        String[] fields = value.toString().split(","); // Split CSV by comma
        if (fields.length == 3) { // Expecting 3 columns: date, HID, consumption
            try {
                String date = fields[0].trim();
                int hid = Integer.parseInt(fields[1].trim());
                double consumption = Double.parseDouble(fields[2].trim()); 

                householdID.set(hid);
                context.write(householdID, new DateConsumptionWritable(date, consumption));
            } catch (NumberFormatException e) {
                System.err.println("Invalid data format: " + value.toString());
            }
        }
    }
}
