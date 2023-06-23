cp /Users/vahid/Documents/config-learner/logs/logs.xlsx /Users/vahid/Documents/config-learner/logs/$(date +%Y-%m-%d--%s).xlsx
#scp -P 24900  vahid@itc-data-6.myket.ir:/home/hossein/config-learner/logs/logs.xlsx /Users/vahid/Documents/config-learner/logs
scp -P 24900  vahid@azd-tempstor-2.myket.ir:/home/vahid/config-learner/logs/logs.xlsx /Users/vahid/Documents/config-learner/logs
