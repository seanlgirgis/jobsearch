# Unix Shell Drills

## 1) grep errors
```bash
grep -i "error" app.log
```
## 2) awk column
```bash
awk -F',' '{print $1,$3}' data.csv
```
## 3) sed replace
```bash
sed 's/old/new/g' input.txt > output.txt
```
## 4) cut field
```bash
cut -d',' -f1,4 data.csv
```
## 5) sort
```bash
sort users.txt
```
## 6) uniq count
```bash
sort users.txt | uniq -c
```
## 7) find file
```bash
find /data -name "*.parquet"
```
## 8) head
```bash
head -20 app.log
```
## 9) tail follow
```bash
tail -f app.log
```
## 10) wc lines
```bash
wc -l input.csv
```
## 11) chmod execute
```bash
chmod +x run_etl.sh
```
## 12) env variable
```bash
export RUN_DATE=2026-05-20
echo $RUN_DATE
```
## 13) exit code check
```bash
./run_job.sh
echo $?
```
## 14) shell loop
```bash
for f in /in/*.csv; do echo "$f"; done
```
## 15) if file exists
```bash
if [ -f /in/data.csv ]; then echo ok; else echo missing; fi
```
## 16) count errors
```bash
grep -ci "error" app.log
```
## 17) spark-submit call
```bash
spark-submit etl_job.py --date "$RUN_DATE"
```
## 18) gzip compress
```bash
gzip -c app.log > app.log.gz
```
## 19) redirect output
```bash
./run_etl.sh > run.log 2>&1
```
## 20) cron awareness
```bash
# Example: run daily at 2 AM
0 2 * * * /opt/jobs/run_etl.sh
```
