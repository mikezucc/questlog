# Omen

## Vision
Empower the prefrontal cortex
https://en.wikipedia.org/wiki/Prefrontal_cortex
This brain region has been implicated in planning complex cognitive behavior, personality expression, decision making, and moderating social behavior.

## Mission
Organize professional relationships.

## Solvable Unsolved Challenges
1. Recalling conversations
2. Fragmentation over how things are remembered between different parties
3. Context switching between different relationships (i.e. work vs side_project_1 vs side_project_2)
4. Passive note taking
5. Self improve ability to communicate

## Solutions
1. Annotation of recorded conversations
2. Partitioning conversation into chunks (highlighting)
3. Tagging/ indexing of annotations for recall
4. Association of conversations to longstanding "identities"
5. Annotation and markup of images

## Random thoughts
https://github.com/mikezucc/questlog/blob/master/relationships.txt

## Entities within the tool
1. Conversations
2. Snippets
3. Tags (i.e. "computer vision", "q4 prospects", "ipad redesign", "magazine print review")
4. People
5. Contexts ("zine", "crypto clothing", "omen", "SFCC")

### Discussion about Entities
Conversations are part of a superclass of entity which is denoted as "Frame".
Frame signifies any kind of captured bits from the owner's sensors. Audio is the primary
method of capture since it is passive. However, owner's may be more proactive during a
session whereby they capture notes via other unlinked medium, like a photo or PDF document.
Conversations can be corrected manually by the user.

Conversations can be subdivided into "Snippets".

Tags are phrases or words that can form relationships to Frames/Snippets. Some tags are auto
generated from the output of the transcription API's. Tags created by the user will also automatically
register matched phrases coming out of the transcription API's

People are user defined. They can have associated Tags, Contexts, Frames, and Snippets.
They are one of the primary methods of organization.

Contexts are user defined. They are the most encompassing organization. These are meant
to be be containers for Frames, Snippets. Examples of a Context include "Magazine Print Project",
"Alexa Partnership Meetings", "Coffee Chats"





"""
