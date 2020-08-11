import time
from libsvc.daemon import Dispatcher

def test_handler():
    D = Dispatcher()
    D.gateway.flushdb()
    D.add_subscriber("test person", "my email", "my inst", ["abc.*", "123"])

    message_data1 = {"dog": "hungry"}
    D.submit_message(["abc.def"], message_data1)  # Check pattern subscription
    message_data2 = {"cat": "orange"}
    D.submit_message(["123"], message_data2)      # Check channel subscription

    time.sleep(0.2)

    m = D.handle_messages(dry_run=True)
    assert("{'dog': 'hungry'}" in str(m[0]))
    assert("{'cat': 'orange'}" in str(m[1]))

def test_subscription():

    D = Dispatcher()
    D.gateway.flushdb()
    s = D.mk_subscriber("test person", "my email", "my inst", ["abc.*", "123"])

    print( s.p.__dict__ )

    message_data1 = {"dog": "hungry"}
    D.submit_message(["abc.def"], message_data1)  # Check pattern subscription
    time.sleep(0.2)
    assert( D.get_messages(s)[0] == message_data1 )

    message_data2 = {"cat": "orange"}
    D.submit_message(["123"], message_data2)      # Check channel subscription
    time.sleep(0.2)
    assert( D.get_messages(s)[0] == message_data2 )


if __name__ == "__main__":

    test_handler()
