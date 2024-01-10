import logging
import datetime

def create_logger(script_name = ''):
    # 로그 생성
    logger = logging.getLogger()
    # 로그의 출력 기준 설정
    logger.setLevel(logging.INFO)
    # log 출력 형식
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # log 출력
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    now = datetime.datetime.now()
    log_file_name = now.strftime("log_%Y_%m_%d_%H_%M_%S.log")
    # log를 파일에 출력
    file_handler = logging.FileHandler(f'./log/{script_name}_{log_file_name}.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

def create_alert_message(channel, alert_text, author):
    ### Example usage:
    alert_message = create_alert_message("ai_alert", "truck counting", "jiwon")
    print(alert_message)

    return {
        "channel": channel,
        "attachments": [
            {
                "color": "#EF002B",
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "Important Alert!",
                            "emoji": True
                        }
                    },
                    {
                        "type": "rich_text",
                        "elements": [
                            {
                                "type": "rich_text_section",
                                "elements": [
                                    {
                                        "type": "text",
                                        "text": alert_text
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "plain_text",
                                "text": f"Author: {author}",
                                "emoji": True
                            }
                        ]
                    }
                ]
            }
        ]
    }

