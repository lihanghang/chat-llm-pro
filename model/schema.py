"""
define extract schema.
"""

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

"""
医疗文本抽取测试
"""
medical_event_schema = Object(
    id="medical",
    description=(
        '''从医疗领域文本中抽取时间time，事件名称event和描述信息description。比如：
        该陪申特于2025年3月19日，因咽喉疼痛来门诊就诊，经诊断为上呼吸道感染，给予静脉滴注0.9%氯化钠注射液250ml，注射用乳糖酸JQKA0.25g，输液50ml时，陪申特出现恶心，呕吐症状，遵医嘱立即停止用药，给予肌肉注射地塞米松5mg，10分钟后，症状缓解。
        [
            {
              "time": "2025年3月19日",
              "event": "就诊",
              "description": "咽喉疼痛"
             },
            {
              "time": "",
              "event": "诊断",
              "description": "上呼吸道感染"
             },
        {
          "time": "",
          "event": "治疗",
          "description": "静脉滴注0.9%氯化钠注射液250ml，注射用乳糖酸JQKA0.25g"
         },
        {
          "time": "输液50ml时",
          "event": "药品不良事件",
          "description": "恶心，呕吐症状"
         },
        
        {
          "time": "",
          "event": "治疗药品不良事件",
          "description": "立即停止用药，给予肌肉注射地塞米松5mg"
         },
        {
          "time": "10分钟后",
          "event": "转归",
          "description": "症状缓解"
         },
        {
          "time": "",
          "event": "治疗",
          "description": "曾自服阿莫西林药物后"
         },
        {
          "time": "",
          "event": "药品不良事件",
          "description": "症状未见好转"
         },
        {
          "time": "",
          "event": "诊断",
          "description": "诊为急性支气管炎"
         },
        {
          "time": "",
          "event": "体检",
          "description": "体温正常"
         }]'''),
    attributes=[
        Text(
            id="time",
            description="事件的发生时间。如20分钟后，30分钟后，2030年11月08日上午8:00等",
            examples=[],
            many=False
        ),
        Text(
            id="event",
            description="事件的名称。如就诊，体检，药品不良事件，治疗药品不良事件，操作，出院，转归等。",
            examples=[],
            many=False,
        ),
        Text(
            id="description",
            description="事件的具体内容。",
            examples=[],
            many=False,
        )
    ],
    examples=[],
    many=True
)
