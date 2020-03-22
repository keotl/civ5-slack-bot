# Sid Meier's Slack Bot
Slack bot to provide Sid Meier's Civilization 5 turn notifications.

![screenshot](https://github.com/keotl/civ5-slack-bot/raw/master/screenshot.png)

## Requirements
- [Sid Meier's Web Hooks](https://github.com/keotl/civ5-webhook)
- Slack (bot permissions with scope `chat.write`)
- Python3.6 and up

## How to use
1. Update the application.yml file to include your slack preferences.
2. This repository can be deployed as-is to services like dokku/heroku/Amazon EBS.
3. Direct [Sid Meier's Web Hooks](https://github.com/keotl/civ5-webhook) to your application, on path `/civ/my-game-name`. 
