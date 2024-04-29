package com.example.hadoop;

import org.apache.hadoop.io.WritableComparable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.DoubleWritable;

import java.io.*;

public class DateConsumptionWritable implements WritableComparable<DateConsumptionWritable> {
    private Text date;
    private DoubleWritable consumption;

    public DateConsumptionWritable() {
        date = new Text();
        consumption = new DoubleWritable();
    }

    public DateConsumptionWritable(String date, double consumption) {
        this.date = new Text(date);
        this.consumption = new DoubleWritable(consumption);
    }

    public Text getDate() {
        return date;
    }
    public DoubleWritable getConsumption() {
        return consumption;
    }

    @Override
    public void write(DataOutput out) throws IOException {
        date.write(out);
        consumption.write(out);
    }

    @Override
    public void readFields(DataInput in) throws IOException {
        date.readFields(in);
        consumption.readFields(in);
    }

    @Override
    public int compareTo(DateConsumptionWritable other) {
        return Double.compare(this.consumption.get(), other.consumption.get());
    }

    @Override
    public String toString() {
        return date.toString() + "\t" + consumption.toString();
    }
}
