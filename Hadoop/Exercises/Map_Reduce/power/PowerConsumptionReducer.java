package com.example.hadoop;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

public class PowerConsumptionReducer extends Reducer<IntWritable, DateConsumptionWritable, IntWritable, Text> {
    @Override
    public void reduce(IntWritable key, Iterable<DateConsumptionWritable> values, Context context) throws IOException, InterruptedException {
        DateConsumptionWritable maxConsumption = null;

        for (DateConsumptionWritable value : values) {
            // Find the value with the maximum consumption
            if (maxConsumption == null || value.getConsumption().get() > maxConsumption.getConsumption().get()) {
                maxConsumption = new DateConsumptionWritable(value.getDate().toString(), value.getConsumption().get());
            }
        }

        if (maxConsumption != null) {
            context.write(key, new Text(maxConsumption.getDate().toString())); // Return the date with the max consumption
        }
    }
}
