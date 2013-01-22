Implementing data cleaning technics 
====================================

1. Parsing
2. Discrepancy detection (`ValidationPipeline`)
3. Spam detection (`DropSpamPipeline`)
4. Clusterring of data (`Clusterring`)
5. Smoothing by bin medians (`Smoothing`)


How to run?
---------------
`scrapy crawl mobile_phones -o items.json -t json`

Dependencies
--------------
To run the `process_data.py` it is required to have a valid json file where from the data is read. If you run the spider like it was shown above, 
everything's gonna be alright.
