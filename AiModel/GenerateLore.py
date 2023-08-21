
from . import CustomModelClass
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.prompts import PromptTemplate

from .locationRelation import *

class loreGenerator():

    def __init__(self) -> None:
        self.affinityObj = None
        self.llm = CustomModelClass.CustomLLM()


    def generateNameList(self, genre):
        

        template = """ 
        [INST] <<SYS>>
        You are name generator.
        Be imaginative and creative. Output the names in a python list format, 
        Skip the header and the starting greetings.
        for example:
        place1 , place2, ...

        Output only the list, do not say anything else.
        <</SYS>>

        Generate 10 location names that fit the {genre} genre [/INST]
        """
        prompt_template = PromptTemplate(input_variables=["genre"], template=template)
        question_chain = LLMChain(llm=self.llm, prompt=prompt_template)

        nameOutput = question_chain.run(genre)

        nameList = nameOutput.split(",")
        nameList = [x.replace("'", "").replace("[", "").replace("]", "") for x in nameList]

        print(nameList)
        self.affinityObj = locationRelation(nameList)
        self.affinityObj.createAffinityGraph()
        return nameList


    def generateLore(self, placeName):
        friend, enemy = self.affinityObj.getCorrespondingLocations(placeName)

        template = """ 
        [INST] <<SYS>>
        You are lore generator. You will be given a place name, output the lore of that place
        Be imaginative and creative. Keep it short. The place has enemies and friends, add descriptions 
        about the place's relations with its enemies and friend locations.
        Skip the header and the starting greetings.
        for example:
        lore....

        Output only the lore, do not say anything else.
        <</SYS>>

        Generate lore for the place called {placeName}, the place is enemies with {enemy} and has affinity towards {friend}
        [/INST]
        """
        prompt_template = PromptTemplate(input_variables=["placeName", "enemy", "friend"], template=template)
        question_chain = LLMChain(llm=self.llm, prompt=prompt_template)

        output = question_chain.run({"placeName":placeName, 
                                     "enemy": enemy, 
                                     "friend": friend})
        return output


# placeList = generateNameList("Fantasy")
# generateLore(placeList[1])
# llm = CustomModelClass.CustomLLM()
# print(llm("what is your name"))