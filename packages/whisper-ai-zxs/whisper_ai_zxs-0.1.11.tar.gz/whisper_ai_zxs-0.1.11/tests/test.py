from whisper_ai_zxs.agent_test import AgentTest
#from ..whisper_ai_zxs.agent_servicer_YD import Agent_YD
from whisper_ai_zxs.agent_servicer_TestStub import Agent_TestStub


Agent = Agent_TestStub("植想说天猫店:亮亮")

Test = AgentTest(Agent)

Test.test()
