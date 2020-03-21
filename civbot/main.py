from jivago.jivago_application import JivagoApplication

import civbot.app

application = JivagoApplication(civbot.app)

if __name__ == '__main__':
    application.run_dev(host="0.0.0.0", port=4000)
