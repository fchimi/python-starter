from openai import AzureOpenAI
import re


AI = None

class Config:
    ROLE = """
When requested to write code, pick Python.
When requested to show chess position, always use the FEN notation.
When showing HTML, always include what is in the body tag,
but exclude the code surrounding the actual content. 
So exclude always BODY, HEAD and HTML .
"""
    MODEL = "gpt-35-turbo"
    API_VERSION ="2023-12-01-preview"

class ChatBot:
    def __init__(self, args, key, host):
        # accesso parametri
        self.key = args.get("OPENAI_API_KEY")
        self.host = args.get("OPENAI_API_HOST")
        # accesso alla ai
        self.ai = AzureOpenAI(api_version=Config.API_VERSION, api_key=self.key, azure_endpoint=self.host)

    def req(msg):
        return [{"role": "system", "content": Config.ROLE}, 
                {"role": "user", "content": msg}]

    def ask(self,input):
        comp = self.ai.chat.completions.create(model=Config.MODEL, messages=self.req(input))
        if len(comp.choices) > 0:
            content = comp.choices[0].message.content
            return content
        return "ERROR"

    def chat(self, args):
        input = args.get("input", "")
        if input == "":
            res = {
                "output": "Welcome to the OpenAI demo chat",
                "title": "OpenAI Chat",
                "message": "You can chat with OpenAI."
            }
        else:
            output = self.ask(input)
            res = self.pextract(output)
            res['output'] = output

        return {"body": res }

    def extract(self,text):
        res = {}
        
        # search for a chess position
        pattern = r'(([rnbqkpRNBQKP1-8]{1,8}/){7}[rnbqkpRNBQKP1-8]{1,8} [bw] (-|K?Q?k?q?) (-|[a-h][36]) \d+ \d+)'
        m = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
        #print(m)
        if len(m) > 0:
            res['chess'] = m[0][0]
            return res

        # search for code
        pattern = r"```(\w+)\n(.*?)```"
        m = re.findall(pattern, text, re.DOTALL)
        if len(m) > 0:
            if m[0][0] == "html":
                html = m[0][1]
                # extract the body if any
                pattern = r"<body.*?>(.*?)</body>"
                m = re.findall(pattern, html, re.DOTALL)
                if m:
                    html = m[0]
                res['html'] = html
                return res
            res['language'] = m[0][0]
            res['code'] = m[0][1]
            return res
        return res


