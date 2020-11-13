from construct import *
from struct import unpack

ResponseParser = Struct( 
        "header" / Int32sb,
        "packet_count" / Int8sb,
        "seq_no" / Int8sb,
        "params" / RepeatUntil(lambda x, lst, ctx: len(lst) == this.packet_count, Struct(
            "category" / Enum(Int8sb, 
                CAR = 0x1,
                ROCKET = 0x2,
                BOMB = 0x3
            ),
             "data" / Switch(this.category, {
                 "CAR" : Struct(
                    "Player_ID" / Int8sb,
                    "Speed" / Int8sb,
                    "X" / Int16sb,
                    "Y" / Int16sb,
                    "checkpoint_ID" / Int8sb,
                    "HP" / Int8sb,
                    "mines" / Int8sb,
                    "rockets" / Int8sb,
                    "Angle" / Int8sb,
                    "Desired_angle" / Int8sb
                 ),
                 "ROCKET" : Struct(
                    "Player_ID" / Int8sb,
                    "Speed" / Int8sb,
                    "X" / Int16sb,
                    "Y" / Int16sb
                 ),
                 "BOMB" : Struct(
                    "Player_ID" / Int8sb,
                    "Speed" / Int8sb,
                    "X" / Int16sb,
                    "Y" / Int16sb
                 )
             }),
        ))
)