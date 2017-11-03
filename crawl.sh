echo '----------begin to crawl----------';

for i in `scrapy list`;
do
echo scrapy crawl $i;
scrapy crawl $i;
done

echo '----------end to crawl----------';
