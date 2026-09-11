#!/usr/bin/env python3
"""
Real-world Digital Library Dataset Generator with Dictionary definitions
Generates a robust, realistic synthetic CSV dataset for a digital library
using 40 of the most famous real-world books that exist.
Fields include: resource_id, title, author, source, topic, reading_level,
excerpt, keywords, language, format, summary, and dictionary (JSON string).
"""

import csv
import json
import os

# Curated list of 40 famous real-world books across various topics
FAMOUS_BOOKS = [
    {
        "title": "A Brief History of Time",
        "author": "Stephen Hawking",
        "source": "Bantam Books",
        "topic": "Science",
        "reading_level": "High School",
        "excerpt": "A well-known scientist (some say it was Bertrand Russell) once gave a public lecture on astronomy. He described how the earth orbits around the sun and how the sun, in turn, orbits around the center of a vast collection of stars called our galaxy.",
        "summary": "An landmark book by physicist Stephen Hawking that explains complex concepts of cosmology, including the Big Bang, black holes, and light cones, to non-specialist readers.",
        "keywords": "physics, cosmology, space, black holes, time, hawking",
        "language": "English",
        "format": "PDF",
        "dictionary": json.dumps({
            "astronomy": "The branch of science that deals with celestial objects, space, and the physical universe.",
            "galaxy": "A system of millions or billions of stars, together with gas and dust, held together by gravitational attraction.",
            "orbits": "Moves in a curved path around a star, planet, or moon."
        })
    },
    {
        "title": "The Origin of Species",
        "author": "Charles Darwin",
        "source": "John Murray Publishing",
        "topic": "Science",
        "reading_level": "Academic",
        "excerpt": "When on board H.M.S. 'Beagle,' as naturalist, I was much struck with certain facts in the distribution of the organic beings inhabiting South America, and in the geological relations of the present to the past inhabitants of that continent.",
        "summary": "Charles Darwin's seminal work introducing the scientific theory of evolution by natural selection, which serves as the foundation of modern evolutionary biology.",
        "keywords": "biology, evolution, natural selection, genetics, science, darwin",
        "language": "English",
        "format": "EPUB",
        "dictionary": json.dumps({
            "naturalist": "An expert in or student of natural history, typically studying plants and animals.",
            "geological": "Relating to the study of the Earth's physical structure, substance, history, and the processes that act on it.",
            "inhabiting": "Living or residing in a particular place."
        })
    },
    {
        "title": "Cosmos",
        "author": "Carl Sagan",
        "source": "Random House",
        "topic": "Science",
        "reading_level": "High School",
        "excerpt": "The Cosmos is all that is or was or ever will be. Our feeblest contemplations of the Cosmos stir us—there is a tingling in the spine, a catch in the voice, a faint sensation, as if a distant memory, of falling from a height.",
        "summary": "Carl Sagan explores the universe, the history of science, and the human search for our place in the cosmos, highlighting the interconnection of science, philosophy, and history.",
        "keywords": "astronomy, space, science, cosmos, human-history, sagan",
        "language": "English",
        "format": "PDF",
        "dictionary": json.dumps({
            "cosmos": "The universe seen as a well-ordered whole.",
            "contemplations": "The action of looking thoughtfully at something for a long time.",
            "sensation": "A physical feeling or perception resulting from something that happens to or comes into contact with the body."
        })
    },
    {
        "title": "The Selfish Gene",
        "author": "Richard Dawkins",
        "source": "Oxford University Press",
        "topic": "Science",
        "reading_level": "High School",
        "excerpt": "We are survival machines—robot vehicles blindly programmed to preserve the selfish molecules known as genes. This is a truth which still fills me with astonishment.",
        "summary": "Richard Dawkins introduces the gene-centered view of evolution, explaining how genes use organisms as vehicles to replicate themselves, and introduces the term 'meme'.",
        "keywords": "biology, evolution, genetics, science, dawkins",
        "language": "English",
        "format": "EPUB",
        "dictionary": json.dumps({
            "molecules": "Groups of atoms bonded together, representing the smallest fundamental unit of a chemical compound.",
            "preserve": "Maintain something in its original or existing state.",
            "astonishment": "Great surprise or wonder."
        })
    },
    {
        "title": "The Double Helix",
        "author": "James D. Watson",
        "source": "Atheneum Books",
        "topic": "Science",
        "reading_level": "High School",
        "excerpt": "I have never seen Francis Crick in a modest mood. Perhaps in other company he is that way, but I have never had reason to believe it. He is a person who talks rapidly, has an loud voice, and who dominates the conversation.",
        "summary": "An autobiographical account of the discovery of the double helix structure of DNA by James Watson and Francis Crick, detailing the personal and academic rivalry behind the breakthrough.",
        "keywords": "biology, genetics, science, dna, history-of-science, watson",
        "language": "English",
        "format": "PDF",
        "dictionary": json.dumps({
            "modest": "Unassuming or moderate in the estimation of one's abilities or achievements.",
            "dominates": "Have a commanding influence on; exercise control over."
        })
    },
    {
        "title": "Silent Spring",
        "author": "Rachel Carson",
        "source": "Houghton Mifflin",
        "topic": "Science",
        "reading_level": "High School",
        "excerpt": "There was once a town in the heart of America where all life seemed to live in harmony with its surroundings. The town lay in the midst of a checkerboard of prosperous farms, with fields of grain and hillsides of orchards.",
        "summary": "A landmark environmental science book detailing the adverse effects of indiscriminate pesticide use on the ecosystem, which helped launch the modern environmental movement.",
        "keywords": "ecology, environment, science, conservation, pesticide, carson",
        "language": "English",
        "format": "EPUB",
        "dictionary": json.dumps({
            "harmony": "Agreement or concord; living peacefully together.",
            "prosperous": "Successful in material terms; flourishing financially.",
            "orchards": "A piece of land planted with fruit trees."
        })
    },
    {
        "title": "Sapiens: A Brief History of Humankind",
        "author": "Yuval Noah Harari",
        "source": "Harvill Secker",
        "topic": "History",
        "reading_level": "High School",
        "excerpt": "About 13.5 billion years ago, matter, energy, time and space came into being in what is known as the Big Bang. The story of these fundamental features of our universe is called physics.",
        "summary": "Yuval Noah Harari surveys the history of humankind from the evolutionary origins of Homo sapiens to the present day, focusing on the cognitive, agricultural, and scientific revolutions.",
        "keywords": "anthropology, evolution, history, humans, society, harari",
        "language": "English",
        "format": "EPUB",
        "dictionary": json.dumps({
            "fundamental": "Forming a necessary base or core; of central importance.",
            "evolutionary": "Relating to the gradual development of something."
        })
    },
    {
        "title": "Guns, Germs, and Steel",
        "author": "Jared Diamond",
        "source": "W. W. Norton & Company",
        "topic": "History",
        "reading_level": "Academic",
        "excerpt": "We all know that history has proceeded very differently for peoples from different parts of the world. In the 13,000 years since the end of the last Ice Age, some parts of the world developed literate industrial societies with metal tools.",
        "summary": "Jared Diamond argues that geographical and environmental factors, rather than genetic differences, shaped the modern world and the unequal development of human societies.",
        "keywords": "geography, history, civilizations, inequality, agriculture, science",
        "language": "English",
        "format": "PDF",
        "dictionary": json.dumps({
            "proceeded": "Began a course of action or moved forward.",
            "literate": "Able to read and write."
        })
    },
    {
        "title": "A People's History of the United States",
        "author": "Howard Zinn",
        "source": "Harper & Row",
        "topic": "History",
        "reading_level": "Academic",
        "excerpt": "Arawak men and women, naked, tawny, and full of wonder, emerged from their villages onto the island's beaches and swam out to get a closer look at the strange big boat.",
        "summary": "Howard Zinn re-examines American history from the perspective of marginalized groups, including Native Americans, slaves, women, and workers, rather than political elites.",
        "keywords": "history, america, social-movements, labor, colonization",
        "language": "English",
        "format": "EPUB",
        "dictionary": json.dumps({
            "tawny": "An orange-brown or yellowish-brown color.",
            "emerged": "Move out of or away from something and become visible."
        })
    },
    {
        "title": "The Rise and Fall of the Third Reich",
        "author": "William L. Shirer",
        "source": "Simon & Schuster",
        "topic": "History",
        "reading_level": "Academic",
        "excerpt": "The birth of the Third Reich, which was to last a thousand years but which survived for only twelve, occurred on the afternoon of January 30, 1933, when Adolf Hitler was sworn in as Chancellor of Germany.",
        "summary": "A detailed history of Nazi Germany from its origins to its defeat in World War II, based on captured German archives and personal observations.",
        "keywords": "history, ww2, germany, hitler, fascism",
        "language": "English",
        "format": "PDF",
        "dictionary": json.dumps({
            "reich": "The German state or empire, especially the Weimar Republic or the Third Reich.",
            "chancellor": "The head of the government in some European countries, such as Germany."
        })
    },
    {
        "title": "The Diary of a Young Girl",
        "author": "Anne Frank",
        "source": "Contact Publishing",
        "topic": "History",
        "reading_level": "Middle School",
        "excerpt": "I hope I will be able to confide everything to you, as I have never been able to confide in anyone, and I hope you will be a great source of comfort and support.",
        "summary": "The personal diary of Anne Frank, a Jewish girl who went into hiding with her family during the Nazi occupation of the Netherlands in World War II.",
        "keywords": "biography, diary, holocaust, ww2, history, anne-frank",
        "language": "English",
        "format": "TXT",
        "dictionary": json.dumps({
            "confide": "Tell someone about a secret or private matter while trusting them not to repeat it to others."
        })
    },
    {
        "title": "The Republic",
        "author": "Plato",
        "source": "Cambridge University Press",
        "topic": "Philosophy",
        "reading_level": "Academic",
        "excerpt": "I went down yesterday to the Piraeus with Glaucon the son of Ariston, that I might offer up my prayers to the goddess; and also because I wanted to see in what manner they would celebrate the festival, which was a new thing.",
        "summary": "Plato's classic Socratic dialogue concerning justice, the order and character of the just city-state, and the nature of the philosopher king.",
        "keywords": "philosophy, justice, politics, greece, classical, plato",
        "language": "English",
        "format": "EPUB",
        "dictionary": json.dumps({
            "piraeus": "The port city of Athens in ancient Greece.",
            "celebrate": "Acknowledge a significant or happy day or event with a social gathering."
        })
    },
    {
        "title": "Meditations",
        "author": "Marcus Aurelius",
        "source": "Oxford University Press",
        "topic": "Philosophy",
        "reading_level": "High School",
        "excerpt": "From my grandfather Verus I learned good morals and the government of my temper. From the reputation and memory of my father, modesty and a manly character. From my mother, piety and beneficence.",
        "summary": "A series of personal writings by the Roman Emperor Marcus Aurelius, offering Stoic philosophy and practical guidance on self-discipline, duty, and resilience.",
        "keywords": "philosophy, stoicism, rome, self-discipline, wisdom",
        "language": "English",
        "format": "TXT",
        "dictionary": json.dumps({
            "piety": "The quality of being religious or reverent.",
            "beneficence": "The quality of doing good or showing active kindness."
        })
    },
    {
        "title": "Beyond Good and Evil",
        "author": "Friedrich Nietzsche",
        "source": "C. G. Naumann",
        "topic": "Philosophy",
        "reading_level": "Academic",
        "excerpt": "Supposing that Truth is a woman—what then? Is there not ground for suspecting that all philosophers, in so far as they have been dogmatists, have failed to understand women—that the terrible seriousness and clumsy importunity with which they have usually paid their addresses to Truth, have been unskilled and unseemly methods for winning a woman?",
        "summary": "Friedrich Nietzsche critiques traditional morality and Western philosophy, advocating for the 'free spirit' and introducing concepts like the will to power.",
        "keywords": "philosophy, morality, psychology, existentialism, nietzsche",
        "language": "English",
        "format": "PDF",
        "dictionary": json.dumps({
            "dogmatists": "People who lay down principles as incontrovertibly true, without consideration of evidence.",
            "importunity": "Persistence in requesting or demanding, especially to the point of annoyance."
        })
    },
    {
        "title": "Critique of Pure Reason",
        "author": "Immanuel Kant",
        "source": "Johann Friedrich Hartknoch",
        "topic": "Philosophy",
        "reading_level": "Academic",
        "excerpt": "Human reason has this peculiar fate that in one species of its knowledge it is burdened by questions which, as prescribed by the very nature of reason itself, it is not able to ignore, but which, as transcending all its powers, it is also not able to answer.",
        "summary": "Immanuel Kant's foundational philosophical work investigating the limits and scope of human understanding and the relationship between rationalism and empiricism.",
        "keywords": "philosophy, epistemology, metaphysics, rationalism, kant",
        "language": "English",
        "format": "PDF",
        "dictionary": json.dumps({
            "prescribed": "State authoritatively as a rule that should be carried out.",
            "transcending": "Going beyond the range or limits of."
        })
    },
    {
        "title": "The Prince",
        "author": "Niccolò Machiavelli",
        "source": "Antonio Blado d'Asola",
        "topic": "Philosophy",
        "reading_level": "High School",
        "excerpt": "It is customary for those who wish to gain the favour of a prince to present themselves before him with those things which they value most, or in which they perceive him to take most delight.",
        "summary": "A 16th-century political treatise offering pragmatic, sometimes ruthless advice to rulers on how to acquire and maintain political power.",
        "keywords": "philosophy, political-theory, renaissance, leadership, machiavelli",
        "language": "English",
        "format": "PDF",
        "dictionary": json.dumps({
            "customary": "According to the customs or usual practices associated with a particular society, place, or set of circumstances.",
            "delight": "Great pleasure."
        })
    },
    {
        "title": "1984",
        "author": "George Orwell",
        "source": "Secker & Warburg",
        "topic": "Fiction",
        "reading_level": "High School",
        "excerpt": "It was a bright cold day in April, and the clocks were striking thirteen. Winston Smith, his chin nuzzled into his breast in an effort to escape the vile wind, slipped quickly through the glass doors of Victory Mansions.",
        "summary": "A dystopian novel depicting a totalitarian regime led by Big Brother, exploring themes of mass surveillance, censorship, and the manipulation of truth and language.",
        "keywords": "literature, dystopia, political-fiction, surveillance, orwell",
        "language": "English",
        "format": "PDF",
        "dictionary": json.dumps({
            "nuzzled": "Leaned or rubbed against gently.",
            "vile": "Extremely unpleasant or bad."
        })
    },
    {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "source": "J. B. Lippincott & Co.",
        "topic": "Fiction",
        "reading_level": "Middle School",
        "excerpt": "When he was nearly thirteen, my brother Jem got his arm badly broken at the elbow. When it healed, and Jem's fears of never being able to play football were assuaged, he was seldom self-conscious about his injury.",
        "summary": "Set in the American South, this novel follows young Scout Finch and her lawyer father Atticus as they confront racial injustice and the loss of innocence in their small town.",
        "keywords": "novel, classics, justice, racism, coming-of-age, harper-lee",
        "language": "English",
        "format": "EPUB",
        "dictionary": json.dumps({
            "assuaged": "Made an unpleasant feeling less intense."
        })
    },
    {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "source": "Charles Scribner's Sons",
        "topic": "Fiction",
        "reading_level": "High School",
        "excerpt": "In my younger and more vulnerable years my father gave me some advice that I've been turning over in my mind ever since. 'Whenever you feel like criticizing any one,' he told me, 'just remember that all the people in this world haven't had the advantages that you've had.'",
        "summary": "A story of the mysterious millionaire Jay Gatsby and his tragic obsession with the beautiful Daisy Buchanan, exploring themes of wealth, love, and the American Dream in the 1920s.",
        "keywords": "literature, novel, classics, 1920s, american-dream, fitzgerald",
        "language": "English",
        "format": "PDF",
        "dictionary": json.dumps({
            "vulnerable": "Susceptible to physical or emotional attack or harm."
        })
    },
    {
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "source": "T. Egerton Publishing",
        "topic": "Fiction",
        "reading_level": "High School",
        "excerpt": "It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife. However little known the feelings or views of such a man may be on his first entering a neighbourhood...",
        "summary": "A romantic novel of manners following the turbulent relationship between Elizabeth Bennet and the wealthy, proud Mr. Darcy in 19th-century England.",
        "keywords": "novel, romance, classics, literature, austen",
        "language": "English",
        "format": "EPUB",
        "dictionary": json.dumps({
            "universally": "By everyone; in every case."
        })
    },
    {
        "title": "Frankenstein",
        "author": "Mary Shelley",
        "source": "Lackington, Hughes & Co.",
        "topic": "Fiction",
        "reading_level": "High School",
        "excerpt": "You will rejoice to hear that no disaster has accompanied the commencement of an enterprise which you have regarded with such evil forebodings. I arrived here yesterday, and my first task is to assure my dear sister of my welfare.",
        "summary": "Mary Shelley's classic gothic novel detailing the tragic experiment of Victor Frankenstein as he creates a sentient creature, exploring the bounds of science and humanity.",
        "keywords": "novel, gothic, science-fiction, classics, mary-shelley",
        "language": "English",
        "format": "EPUB",
        "dictionary": json.dumps({
            "commencement": "The beginning of something.",
            "forebodings": "Feelings that something bad is going to happen."
        })
    },
    {
        "title": "Moby-Dick",
        "author": "Herman Melville",
        "source": "Richard Bentley Publisher",
        "topic": "Fiction",
        "reading_level": "High School",
        "excerpt": "Call me Ishmael. Some years ago—never mind how long precisely—having little or no money in my purse, and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world.",
        "summary": "A classic American novel recounting the quest of the obsessive Captain Ahab for revenge on Moby Dick, the giant white whale that bit off his leg.",
        "keywords": "literature, novel, classics, sea-faring, adventure, melville",
        "language": "English",
        "format": "EPUB",
        "dictionary": json.dumps({
            "precisely": "In a exact manner."
        })
    },
    {
        "title": "The Mythical Man-Month",
        "author": "Fred Brooks",
        "source": "Addison-Wesley",
        "topic": "Technology",
        "reading_level": "Academic",
        "excerpt": "The tar pit of software engineering will continue to swallow projects and teams. No single tool or management technique is a silver bullet, but understanding the human aspects of programming remains our defense.",
        "summary": "A classic collection of essays on software engineering project management, highlighting the famous law that adding programmers to a late project makes it later.",
        "keywords": "computer-science, software-engineering, management, programming, technology",
        "language": "English",
        "format": "PDF",
        "dictionary": json.dumps({
            "silver bullet": "A simple and seemingly magical solution to a complicated problem."
        })
    },
    {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "source": "Prentice Hall",
        "topic": "Technology",
        "reading_level": "High School",
        "excerpt": "Bad code can ruin a development team. The clutter builds, productivity plunges, and eventually, the system must be completely rewritten. Writing clean code is not just a matter of rules; it requires craftsmanship.",
        "summary": "A handbook of agile software craftsmanship that guides developers on how to write professional, clean, and maintainable code with practical examples.",
        "keywords": "programming, software-engineering, clean-code, agile, technology",
        "language": "English",
        "format": "EPUB",
        "dictionary": json.dumps({
            "craftsmanship": "Skill in a particular craft; professional execution quality."
        })
    },
    {
        "title": "Introduction to Algorithms",
        "author": "Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein",
        "source": "MIT Press",
        "topic": "Technology",
        "reading_level": "Academic",
        "excerpt": "An algorithm is any well-defined computational procedure that takes some value, or set of values, as input and produces some value, or set of values, as output. An algorithm is thus a sequence of computational steps that transform the input into the output.",
        "summary": "A comprehensive, rigorous introduction to the design and analysis of computer algorithms, widely used as a standard textbook in universities.",
        "keywords": "technology, computer-science, algorithms, mathematics, data-structures",
        "language": "English",
        "format": "PDF",
        "dictionary": json.dumps({
            "computational": "Relating to or using computers or mathematical calculation."
        })
    },
    {
        "title": "Design Patterns",
        "author": "Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides",
        "source": "Addison-Wesley",
        "topic": "Technology",
        "reading_level": "Academic",
        "excerpt": "Designing object-oriented software is hard, and designing reusable object-oriented software is even harder. You must find pertinent objects, factor them into classes at the right granularity, define class interfaces and inheritance hierarchies...",
        "summary": "A landmark computer science textbook describing 23 classic design patterns in object-oriented programming to solve common software design problems.",
        "keywords": "computer-science, programming, software-engineering, architecture, technology",
        "language": "English",
        "format": "PDF",
        "dictionary": json.dumps({
            "pertinent": "Relevant or applicable to a particular matter.",
            "granularity": "The scale or level of detail in a set of data or software model."
        })
    },
    {
        "title": "Steve Jobs",
        "author": "Walter Isaacson",
        "source": "Simon & Schuster",
        "topic": "Biography",
        "reading_level": "High School",
        "excerpt": "By the time he was in his early twenties, Steve Jobs was already famous, rich, and eccentric. He had cofounded Apple Computer in his parents' garage, taken it public, and become the face of the personal computer revolution.",
        "summary": "The definitive biography of Apple co-founder Steve Jobs, detailing his intense personality, creative drive, and revolutionary impact on technology and media industries.",
        "keywords": "biography, technology, apple, silicon-valley, innovation, jobs",
        "language": "English",
        "format": "PDF",
        "dictionary": json.dumps({
            "eccentric": "Unconventional and slightly strange behavior."
        })
    },
    {
        "title": "Long Walk to Freedom",
        "author": "Nelson Mandela",
        "source": "Little, Brown & Co",
        "topic": "Biography",
        "reading_level": "High School",
        "excerpt": "I was born on the eighteenth of July 1918 at Mvezo, a tiny village on the banks of the Mbashe River in the district of Umtata, the capital of the Transkei. The year of my birth was the end of the Great War.",
        "summary": "The autobiography of Nelson Mandela, tracing his early life, his resistance against apartheid in South Africa, his 27 years of imprisonment, and his ultimate presidency.",
        "keywords": "biography, autobiography, apartheid, south-africa, civil-rights, mandela",
        "language": "English",
        "format": "EPUB",
        "dictionary": json.dumps({
            "apartheid": "A system of institutionalised racial segregation that existed in South Africa from 1948 until the early 1990s."
        })
    },
    {
        "title": "The Autobiography of Malcolm X",
        "author": "Malcolm X, Alex Haley",
        "source": "Grove Press",
        "topic": "Biography",
        "reading_level": "High School",
        "excerpt": "When my mother was pregnant with me, she told me later, a party of hooded Ku Klux Klan riders galloped up to our house in Omaha, Nebraska, brandishing shotguns and rifles.",
        "summary": "The life story of the prominent African American activist Malcolm X, detailing his journey from street hustler to leader in the Nation of Islam and advocate for Black empowerment.",
        "keywords": "biography, autobiography, civil-rights, race, history, malcolm-x",
        "language": "English",
        "format": "TXT",
        "dictionary": json.dumps({
            "brandishing": "Wave or flourish something, especially a weapon, as a threat or in anger or excitement."
        })
    },
    {
        "title": "Alexander Hamilton",
        "author": "Ron Chernow",
        "source": "Penguin Press",
        "topic": "Biography",
        "reading_level": "High School",
        "excerpt": "His life was a romance, a tragedy, a triumph, and a warning. He was the most brilliant and charismatic of the founding fathers, yet also the most self-destructive.",
        "summary": "A comprehensive biography of the first U.S. Treasury Secretary, Alexander Hamilton, detailing his role in the American Revolution, the Constitution, and his legendary duel with Aaron Burr.",
        "keywords": "biography, history, america, founding-fathers, constitution, hamilton",
        "language": "English",
        "format": "PDF",
        "dictionary": json.dumps({
            "charismatic": "Exercising a compelling charm which inspires devotion in others."
        })
    },
    {
        "title": "The Wealth of Nations",
        "author": "Adam Smith",
        "source": "W. Strahan and T. Cadell",
        "topic": "Philosophy",
        "reading_level": "Academic",
        "excerpt": "The greatest improvement in the productive powers of labour, and the greater part of the skill, dexterity, and judgment with which it is any where directed, or applied, seem to have been the effects of the division of labour.",
        "summary": "Adam Smith's foundational work on economics, describing the division of labor, productivity, and free markets as the key drivers of national wealth.",
        "keywords": "economics, capitalism, markets, productivity, labor",
        "language": "English",
        "format": "PDF",
        "dictionary": json.dumps({
            "dexterity": "Skill in performing tasks, especially with the hands.",
            "division of labour": "The assignment of different parts of a manufacturing process or task to different people in order to improve efficiency."
        })
    },
    {
        "title": "Das Kapital",
        "author": "Karl Marx",
        "source": "Verlag von Otto Meissner",
        "topic": "Philosophy",
        "reading_level": "Academic",
        "excerpt": "The wealth of those societies in which the capitalist mode of production prevails, presents itself as an immense accumulation of commodities, its unit being a single commodity.",
        "summary": "Karl Marx's critical analysis of capitalism, examining how capital is accumulated, the exploitation of labor, and the division of classes.",
        "keywords": "capitalism, labor, economics, class-struggle, marx",
        "language": "English",
        "format": "PDF",
        "dictionary": json.dumps({
            "capitalist": "A person who has capital, especially in business, and supports capitalism.",
            "commodities": "Raw materials or primary agricultural products that can be bought and sold."
        })
    },
    {
        "title": "The Interpretation of Dreams",
        "author": "Sigmund Freud",
        "source": "Franz Deuticke",
        "topic": "Science",
        "reading_level": "High School",
        "excerpt": "In the following pages I shall prove that there is a psychological technique which makes it possible to interpret dreams, and that on the application of this method every dream will reveal itself as a psychological structure, full of significance.",
        "summary": "Sigmund Freud introduces his theory of the unconscious mind, arguing that dreams are forms of wish-fulfillment that can be systematically analyzed.",
        "keywords": "psychology, dreams, unconscious, mind, freud",
        "language": "English",
        "format": "PDF",
        "dictionary": json.dumps({
            "interpret": "Explain the meaning of information or actions.",
            "unconscious": "The part of the mind which is inaccessible to the conscious mind but which affects behavior."
        })
    },
    {
        "title": "Gitanjali",
        "author": "Rabindranath Tagore",
        "source": "India Society of London",
        "topic": "Fiction",
        "reading_level": "Middle School",
        "excerpt": "Thou hast made me endless, such is thy pleasure. This frail vessel thou emptiest again and again, and fillest it ever with fresh life. This little flute of a reed thou hast carried over hills and dales.",
        "summary": "A collection of spiritual poems by Rabindranath Tagore, exploring devotion, humanity, nature, and the connection between the soul and the divine.",
        "keywords": "poetry, literature, tagore, spiritual, india",
        "language": "English",
        "format": "EPUB",
        "dictionary": json.dumps({
            "frail": "Weak and delicate.",
            "vessel": "A container or ship, metaphorically representing the human body or soul."
        })
    },
    {
        "title": "The Odyssey",
        "author": "Homer",
        "source": "Oxford University Press",
        "topic": "Fiction",
        "reading_level": "High School",
        "excerpt": "Tell me, O Muse, of that ingenious hero who travelled far and wide after he had sacked the famous town of Troy. Many cities did he visit, and many were the nations with whose manners and customs he was acquainted.",
        "summary": "Homer's ancient Greek epic poem telling the story of Odysseus' ten-year journey home to Ithaca after the fall of Troy.",
        "keywords": "odyssey, homer, epic, greece, mythology, classics",
        "language": "English",
        "format": "EPUB",
        "dictionary": json.dumps({
            "ingenious": "Clever, original, and inventive.",
            "sacked": "Dismissed or pillaged and destroyed by an army."
        })
    },
    {
        "title": "The Prince and the Pauper",
        "author": "Mark Twain",
        "source": "Chatto & Windus",
        "topic": "Fiction",
        "reading_level": "Middle School",
        "excerpt": "In the ancient city of London, on a certain autumn day in the second quarter of the sixteenth century, a boy was born to a poor family of the name of Canty, who did not want him. On the same day another English child was born to a rich family of the name of Tudor, who did want him.",
        "summary": "A classic novel where a young beggar named Tom Canty and Edward Tudor, the Prince of Wales, exchange identities, experiencing each other's lives.",
        "keywords": "novel, classics, mark-twain, identity, historical-fiction",
        "language": "English",
        "format": "EPUB",
        "dictionary": json.dumps({
            "pauper": "A very poor person.",
            "tudor": "Relating to the English royal dynasty which ruled 1485–1603."
        })
    },
    {
        "title": "The Art of War",
        "author": "Sun Tzu",
        "source": "Lionel Giles Translation",
        "topic": "Philosophy",
        "reading_level": "High School",
        "excerpt": "The art of war is of vital importance to the State. It is a matter of life and death, a road either to safety or to ruin. Hence it is a subject of inquiry which can on no account be neglected.",
        "summary": "An ancient Chinese military treatise attributed to Sun Tzu, detailing strategies for warfare, diplomacy, and conflict resolution.",
        "keywords": "strategy, warfare, leadership, conflict, sun-tzu",
        "language": "English",
        "format": "PDF",
        "dictionary": json.dumps({
            "neglected": "Not receiving proper care or attention.",
            "inquiry": "An act of asking for information."
        })
    },
    {
        "title": "The Elements",
        "author": "Euclid",
        "source": "Cambridge University Press",
        "topic": "Science",
        "reading_level": "Academic",
        "excerpt": "A point is that which has no part. A line is a breadthless length. The extremities of a line are points. A straight line is a line which lies evenly with the points on itself.",
        "summary": "An ancient mathematical treatise consisting of 13 books containing geometry definitions, axioms, theorems, and proofs that laid the foundation of mathematics.",
        "keywords": "mathematics, geometry, proofs, axioms, euclid",
        "language": "English",
        "format": "PDF",
        "dictionary": json.dumps({
            "breadthless": "Having no width or thickness.",
            "extremities": "The furthest limits or points of something."
        })
    },
    {
        "title": "Walden",
        "author": "Henry David Thoreau",
        "source": "Ticknor and Fields",
        "topic": "Philosophy",
        "reading_level": "High School",
        "excerpt": "I went to the woods because I wished to live deliberately, to front only the essential facts of life, and see if I could not learn what it had to teach, and not, when I came to die, discover that I had not lived.",
        "summary": "Thoreau's reflection upon simple living in natural surroundings at Walden Pond, exploring self-reliance and transcendentalist philosophy.",
        "keywords": "nature, simplicity, thoreau, philosophy, transcendentalism",
        "language": "English",
        "format": "PDF",
        "dictionary": json.dumps({
            "deliberately": "Consciously and intentionally; in a careful and unhurried way.",
            "essential": "Absolutely necessary; extremely important."
        })
    },
    {
        "title": "Understanding Media",
        "author": "Marshall McLuhan",
        "source": "McGraw-Hill",
        "topic": "Technology",
        "reading_level": "Academic",
        "excerpt": "In a culture like ours, long accustomed to splitting and dividing all things as a means of control, it is sometimes a bit of a shock to be reminded that, in operational and practical fact, the medium is the message.",
        "summary": "Marshall McLuhan introduces the concept that the form of a medium embeds itself in any message it transmits, creating a symbiotic relationship.",
        "keywords": "media, technology, communication, society, mcluhan",
        "language": "English",
        "format": "PDF",
        "dictionary": json.dumps({
            "medium": "An agency or means of doing something.",
            "accustomed": "Customary or usual."
        })
    }
]

def main():
    target_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(target_dir, "digital_library_starter.csv")
    
    print(f"Creating real-world famous books digital library dataset...")
    print(f"Target Output: {output_file}")
    
    fieldnames = [
        "resource_id", "title", "author", "source", "topic", 
        "reading_level", "excerpt", "keywords", "language", 
        "format", "summary", "dictionary"
    ]
    
    records = []
    for idx, book in enumerate(FAMOUS_BOOKS, start=1):
        topic_code = book["topic"][:3].upper()
        book["resource_id"] = f"RES-{topic_code}-{idx:04d}"
        records.append(book)
        
    try:
        with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for record in records:
                writer.writerow(record)
        print(f"Successfully generated {len(records)} real-world books dataset with dictionary entries.")
        print(f"Fields exported: {', '.join(fieldnames)}")
    except Exception as e:
        print(f"Error writing to CSV: {e}")

if __name__ == "__main__":
    main()
