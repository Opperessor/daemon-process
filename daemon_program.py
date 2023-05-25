import os
import sys
import fcntl
import daemon
import file_operation

PIDFILE = '/files/daemon.pid'
error_file = '/files/error.txt'

def acquire_lock():
    try:
        with open(error_file,'a') as erfile:
            erfile.writelines("entered to acquire lock\n")
        lock_file = open(PIDFILE, 'w')
        fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        lock_file.write(str(os.getpid()))
        lock_file.flush()
        return lock_file
    except IOError:
        #not able to print this statement on the terminal
        print("another file is being processed")
        sys.exit(1)

def release_lock(lock_file):
    fcntl.flock(lock_file, fcntl.LOCK_UN)
    lock_file.close()
    os.remove(PIDFILE)
    with open(error_file, 'a') as erfile:
        erfile.writelines("lock released\n")

def daemon_process(infile):
    file_operation.main_test(infile)

def start_daemon(input_file):
    lock_file = acquire_lock()
    daemon_process(input_file)
    release_lock(lock_file)

def stop_daemon():
    if os.path.exists(PIDFILE):
        with open(PIDFILE, 'r') as lock_file:
            pid = lock_file.read().strip()
        os.remove(PIDFILE)
        with open(error_file,'a') as erfile:
            erfile.writelines(f"Stopping daemon process \n")

    else:
        with open(error_file,'a') as erfile:
            erfile.writelines("No running daemon process found. Exiting. not taken the file\n")

def main():
    if len(sys.argv) > 4 or sys.argv[1] not in ['start', 'stop']:
        print("Usage: python daemon_program.py [start|stop]")
        sys.exit(1)

    if sys.argv[1] == 'start':
        input_file = sys.argv[2]
        with daemon.DaemonContext():
            start_daemon(input_file)

    elif sys.argv[1] == 'stop':
        stop_daemon()

if __name__ == '__main__':
    main()


# python daemon_program.py start /home/james/Videos/daemon_gitHUB/Daemon_process/daemon-process/files/input_file.txt
# python daemon_program.py start /home/james/Videos/daemon_gitHUB/Daemon_process/daemon-process/files/input_file.txt
