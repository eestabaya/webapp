
# Base embed limits
CHAR_LIMIT = 6000
TITLE_LIMIT = 256
DESC_LIMIT = 4096

COUNT_LIMIT = 10

# Embed field limits
FIELD_OBJ_LIMIT = 25
FIELD_NAME_LIMIT = 256
FIELD_VALUE_LIMIT = 1024

# Embed etc limits
FOOTER_TEXT_LIMIT = 2048
AUTHOR_NAME_LIMIT = 256

STR_ERROR = "Embed {} must not be greater than {} characters."
STR_EMPTY = "Embed {} must not be blank."


class EmbedContainer:
    def __init__(self):
        self.embeds = []


    def containerize(self, embeds):
        self.embeds = embeds


    def add_to_container(self, embed):
        self.embeds.append(embed)


    def get_payload(self, timestamp=None):
        # Validation
        if len(self.embeds) > COUNT_LIMIT:
            raise ValueError("Cannot exceed {} embeds in payload.".format(str(COUNT_LIMIT)))

        sums = [e.char_sum() for e in self.embeds]
        if sum(sums) > CHAR_LIMIT:
            raise ValueError(STR_ERROR.format("CHARACTER COUNT", str(CHAR_LIMIT)))

        return [e.get_embed(timestamp=timestamp, validate=False) for e in self.embeds]


class DiscordEmbed:
    def __init__(self, title="", description="", color=0x000000):
        self.title = title
        self.description = description

        if len(title) > TITLE_LIMIT:
            raise ValueError(STR_ERROR.format("TITLE", str(TITLE_LIMIT)))

        if len(description) > DESC_LIMIT:
            raise ValueError(STR_ERROR.format("DESCRIPTION", str(DESC_LIMIT)))

        self.color = color

        self.footer = None
        self.author = None

        self.embed_fields = []


    def get_embed(self, timestamp=None, validate=True):
        if validate:
            self.validate_embed()

        embed_payload = {
            "type": "rich", #TODO review this later

            "title": (self.title if self.title != "" else None),
            "description": (self.description if self.description != "" else None),

            "timestamp": timestamp,
            "color": self.color,

            "footer": self.footer,
            "author": self.author,

            "fields": [
                field.get_field_json() for field in self.embed_fields
            ]
        }
        return embed_payload


    def add_field(self, name, value, inline=False):
        if len(self.embed_fields) >= FIELD_OBJ_LIMIT:
            raise ValueError("Embed must not exceed {} FIELDS.".format(str(FIELD_OBJ_LIMIT)))

        field = EmbedField(name, value, inline)
        self.embed_fields.append(field)


    def set_footer(self, footer_text, icon_url=None, proxy_icon_url=None):
        if footer_text == "":
            raise ValueError(STR_EMPTY.format("FOOTER"))

        self.footer = {
            "text": footer_text,
            "icon_url": icon_url,
            "proxy_icon_url": proxy_icon_url
        }


    def set_author(self, name, url=None, icon_url=None, proxy_icon_url=None):
        self.author = {
            "name": name,
            "url": url,
            "icon_url": icon_url,
            "proxy_icon_url": proxy_icon_url
        }


    def char_sum(self):
        char_count = len(self.title) + len(self.description)

        for field in self.embed_fields:
            char_count = char_count + field.field_char_count()

        if self.footer is not None:
            char_count = char_count + len(self.footer['text'])

        if self.author is not None:
            char_count = char_count + len(self.author['name'])

        return char_count


    def validate_embed(self):
        char_count = self.char_sum()

        if char_count > CHAR_LIMIT:
            raise ValueError(STR_ERROR.format("CHARACTER COUNT", str(CHAR_LIMIT)))


class EmbedField:
    def __init__(self, name, value, inline):
        self.name = name
        self.value = value

        if name == "":
            raise ValueError(STR_EMPTY.format("FIELD NAME"))

        if value == "":
            raise ValueError(STR_EMPTY.format("FIELD VALUE"))

        if len(name) > FIELD_NAME_LIMIT:
            raise ValueError(STR_ERROR.format("FIELD NAME", str(FIELD_NAME_LIMIT)))

        if len(value) > FIELD_VALUE_LIMIT:
            raise ValueError(STR_ERROR.format("FIELD VALUE", str(FIELD_VALUE_LIMIT)))

        self.inline = inline


    def field_char_count(self):
        return len(self.name) + len(self.value)
    
    
    def get_field_json(self):
        return {
            "name": self.name,
            "value": self.value,
            "inline": self.inline
        }
