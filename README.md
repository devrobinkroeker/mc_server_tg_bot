# mc_server_tg_bot
Controls a minecraft server docker container through a telegram bot. [This](https://hub.docker.com/r/itzg/minecraft-server) is the minecraft server docker image. The idea is to run this bot on your server where your minecraft docker container is also running.

Set your telegram bot token as an environment variable named `TG_TOKEN` and your password of choice as `TG_PASS`. You will be asked for your password when starting the bot in telegram with '/start' command.
Run the bot like so: `./bot.py <minecraft_container_name>`
