import requests
from colorama import Fore
import json
import time

monitorURL = 'https://aiomacbot.myshopify.com/products.json'
cartURL = 'https://aiomacbot.myshopify.com/cart/38188288335:1'

delay = 5

slack_webhook = 'YOUR_SLACK_WEBHOOK_HERE'

restock = False

req = requests.Session()

def sendMessage(msg_data):
	print(Fore.CYAN + 'Sending message...')
	res = req.post(slack_webhook, headers={'Content-Type': 'application/json'}, data=json.dumps(msg_data))
	if res.status_code == 200:
		print(Fore.GREEN + str(res.status_code) + ' - Message Sent!')
	else:
		print(Fore.RED + str(res.status_code) + ' - Error Sending Message!')

def monitor():
	res = req.get(monitorURL)
	parsed = json.loads(res.text)
	#print json.dumps(parsed, indent=4, sort_keys=True)
	image = parsed['products'][0]['images'][0]['src']
	title = parsed['products'][0]['title']
	description = parsed['products'][0]['body_html']
	if parsed['products'][0]['variants'][0]['available'] == False:
		print(Fore.CYAN + '{} - ITEM OOS').format(time.strftime('[%I:%M:%S]'))
	elif parsed['products'][0]['variants'][0]['available'] == True:
		print(For.GREEN + '{} - ITEM RESTOCKED').format(time.strftime('[%I:%M:%S]'))
		slack_data = {
		    "attachments": [
		        {
		            "fallback": "{} - RESTOCK FOR TASKBOT!".forrmat(time.strftime('[%I:%M:%S]')),
		            "color": "#228aff",
		            "pretext": "<!everyone>",
		            "author_name": "@spideynuff1",
		            "author_link": "https://github.com/arnav486",
		            #"author_icon": "http://flickr.com/icons/bobby.jpg",
		            "title": "[{}] - RESTOCK FOR ITEM: '{}'\n\n".forrmat(time.strftime('[%I:%M:%S]'), title),
		            #"title_link": "https://api.slack.com/",
		            #"text": "Optional text that appears within the attachment",
		            "fields": [
		                {
		                    "title": "Description",
		                    "value": description,
		                    "short": True
		                },
		                {
		                  "title": "ATC Link",
		                  "value": '<{}|Straight to Cart>'.format(cartURL),
		                  "short": True
		                }
		            ],
		            "thumb_url": image, 
		            "footer": '@spideynuf1\'s Bot Restock Monitor | {}'.format(time.strftime('[%I:%M:%S]')),
		            #"ts": 123456789
		        }
		    ]
		}
		sendMessage(slack_data)
		restock = True
	else:
		print(Fore.RED + '{} - ERROR CHECKING STOCK').format(time.strftime('[%I:%M:%S]'))

if __name__ == '__main__':
	print(Fore.GREEN + '{} - Monitor started! **Made by @spideynuff1**').format(time.strftime('[%I:%M:%S]'))
	print(Fore.CYAN + '{} - Please make sure you have added a Slack/Discord Webhook for the script to send messages.').format(time.strftime('[%I:%M:%S]'))
	time.sleep(3)
	while restock == False:
		monitor()
		time.sleep(delay)






