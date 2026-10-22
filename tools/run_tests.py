from pathlib import Path
import getpass,os,subprocess,sys
root=Path(__file__).resolve().parents[1]
env=dict(os.environ)
if not env.get('BD_TEST_USERNAME'):
    env['BD_TEST_USERNAME']=getpass.getpass('Facilitator username for protected-file UI tests (hidden): ')
if not env.get('BD_TEST_PASSWORD'):
    env['BD_TEST_PASSWORD']=getpass.getpass('Facilitator password for protected-file UI tests (hidden): ')
result=subprocess.run(['node','--test','tests/dashboard.test.mjs'],cwd=root,env=env)
sys.exit(result.returncode)
