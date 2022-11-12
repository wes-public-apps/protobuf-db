from common_pb2 import RawMsg
from complex_pb2 import N4, N6, ComplexMessage
from nested_pb2 import N2, TestNested
from specials_pb2 import TestSpecials
from types_pb2 import N3, TestTypes, TYPES


# common raw msg
def set_raw(obj, id=10, timestamp=23432, data="data"):
    obj.id = id
    obj.timestamp = timestamp
    obj.data = data


raw_msg = RawMsg()
set_raw(raw_msg)


# N4
def set_n4(obj, id=23):
    obj.id = 23
    obj.raw_msgs.extend([RawMsg(), RawMsg()])
    set_raw(obj.raw_msgs[0])
    set_raw(obj.raw_msgs[1], id=11)
    set_raw(obj.raw_msgs_by_id['msg0'])
    set_raw(obj.raw_msgs_by_id['msg1'], id=11)


n4 = N4()
n4_2 = N4()
n4_3 = N4()
set_n4(n4)
set_n4(n4_2)
set_n4(n4_3)
n4_2.raw_msgs.append(RawMsg())
n4_3.raw_msgs.append(RawMsg())
set_raw(n4_2.raw_msgs[2])
set_raw(n4_2.raw_msgs_by_id['a'])
set_raw(n4_3.raw_msgs[2])
set_raw(n4_3.raw_msgs_by_id['a'])
del n4_2.raw_msgs_by_id["msg1"]

# complex complex
complex_msg = ComplexMessage()
set_raw(complex_msg.raw_msgs_by_id['msg0'])
set_raw(complex_msg.raw_msgs_by_id['msg1'], id=11)
complex_msg.n4s.extend([N4(), N4()])
set_n4(complex_msg.n4s[0])
set_n4(complex_msg.n4s[1], id=24)
set_n4(complex_msg.n4s_by_id['msg0'])
set_n4(complex_msg.n4s_by_id['msg1'], id=24)


def set_n5(obj, types=[], data="n5_data"):
    obj.types.extend(types)
    obj.data = data


set_n5(
    complex_msg.n5s_by_id['msg0'],
    types=[
        ComplexMessage.N5.N5Types.Value('type1'),
        ComplexMessage.N5.N5Types.Value('type2')])
set_n5(
    complex_msg.n5s_by_id['msg1'],
    types=[
        ComplexMessage.N5.N5Types.Value('type1'),
        ComplexMessage.N5.N5Types.Value('type2')],
    data="n5_data_1")

# complex N6
n6 = N6()
set_n5(n6.n5val)

# nested N2
n2 = N2()
n2.val2 = "this is n2"

# nested TestNested
test_nested = TestNested()
test_nested.val1.val1 = "this is a nested n1"
test_nested.val2.val2 = "this is a nested n2"

# specials TestSpecial
test_specials = TestSpecials()
test_specials.list1.extend(["1", "2", "3"])
test_specials.map1["key1"] = "val1"
test_specials.map1["key2"] = "val2"
test_specials.map1["key3"] = "val3"
test_specials.fault1 = True

# types N3
n3 = N3()
n3.val1 = 1
n3.val2 = 2

# types TestTypes
test_types = TestTypes()
test_types.val1 = -320
test_types.val2 = 0.032
test_types.val3 = -24
test_types.val4 = -2439723
test_types.val5 = 32845
test_types.val6 = 89345230
test_types.val7 = -32932
test_types.val8 = 329323
test_types.val9 = 843782
test_types.val10 = 348795439
test_types.val11 = -329823
test_types.val12 = -329823238
test_types.val13 = False
test_types.val14 = "hello world"
test_types.val15 = b'jknq3290dskss'
test_types.val16 = TYPES.type1
test_types.val17.val1 = 1
test_types.val17.val2 = 2
test_types.val18["msg1"].val1 = 1
test_types.val18["msg1"].val2 = 2
test_types.val18['msg2'].val1 = 1
test_types.val18['msg2'].val2 = 1
test_types.val19.extend([N3(), N3(), N3()])
