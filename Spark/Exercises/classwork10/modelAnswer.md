## Model Answer 10

1. Most of the code in the Jupyter notebook just had to be run and the outcome had to be inspected. There were a couple of small exercises for which code had to be written:

    - **As a small Exercise**, now group the data according to the country of origins and count the number of flights from every country. Output the top three countries, i.e., the three countries with the most outbound flights. Hint: if you want to sort in descending order, you need an additional parameter:`ascending=False`, e.g.
    ```
    flightData2015.sort("count", ascending=False)
    topOutbound = flightData2015.groupBy("ORIGIN_COUNTRY_NAME").sum("count").sort('sum(count)', ascending=False)
    topOutbound.show(3)
    ```

    - **Just before the introduction to Spark Streaming**:Take the windowing query from above and increase the window size to 40 minutes. Compare the output to the one with a window size of 10 minutes.
    ```
    winCountsSE = withEventTime.groupBy(window(col("event_time"),"40 minutes")).count()
    winQuerySE = winCountsSE.writeStream.queryName("events_per_winSE").format("memory").outputMode("complete").start()
    spark.streams.active
    ```

    - Now formulate the query and run it on the stream.
    ```
    spark.sql("select * from events_per_winSE order by window").show(20,False)
    ```

    As the windows are larger, there are fewer of them (compared to the windows with a size of 10 minutes) and they contain higher counts

    - Do not forget to stop the stream processing once you are done with the exercise.
    ```
    winQuerySE.stop()
    spark.streams.active
    ```
