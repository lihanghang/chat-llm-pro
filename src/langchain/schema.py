from kor import Object, Text

info_schema = Object(
  id="info",
  description=(
      "关于临时公告-停牌信息的抽取--包含了公司名称，停牌日期，停牌天数。"
      " music by a particular artist."
  ),
  attributes=[
      Text(
          id="company_name",
          description="公告涉及的公司名称",
          examples=[],
          many=True,
      ),
      Text(
          id="date",
          description="公告涉及的停牌日期",
          examples=[],
          many=True,
      ),
      Text(
          id="day",
          description="公告涉及的停牌天数",
          examples=[("股票将于2021年4月27日停牌1天", "1天")],
          many=True,
      ),
    ],
  many=False,
)

person_schema = Object(
    id="person",
    description=(
        "关于临时公告-辞职或选举信息的提取--包含了辞职日期，辞职人姓名，辞职人原因，辞去职务，辞职后是否还担任职务，是否持有股份信息，推理出辞职人的性别。"
    ),
    attributes=[
        Text(
            id="name",
            description="辞职人姓名",
            examples=[],
            many=False
        ),
        Text(
            id="date",
            description="包含了辞职日期",
            examples=[],
            many=False,
        ),
        Text(
            id="position",
            description="辞去职务",
            examples=[],
            many=False,
        ),
        Text(
            id="reason",
            description="辞职人原因",
            examples=[],
            many=False,
        ),
        Text(
            id="after_position",
            description="辞职后是否还担任职务",
            examples=[],
            many=False,
        ),
        Text(
            id="share",
            description="是否持有股份",
            examples=[],
            many=False,
        ),
        Text(
            id="sex",
            description="性别，根据辞职人的姓名称谓推理出性别为男、女或空",
            examples=[("先生", "男"), ("女士", "女"), ("博士", "")],
            many=False,
        )
    ],
    many=True
)

#
# txt = '''深圳市京基智农时代股份有限公司（以下简称“公司”）董事会于 2022年10月27日收到公司董事陈家俊先生提交的书面辞职信，陈家俊先生因个人原因辞
# 去公司第十届董事会董事职务。辞职以后，陈家俊先生不再担任公司任何职务。截至本公告披露日，陈家俊先生未持有公司股份。
# 董事会于近日收到公司董事刘宏伟先生的书面辞职申请，刘宏伟博士因退休原因申请辞去公司第九届董事会董事职务，辞职后不在公司担任任何职务。'''

