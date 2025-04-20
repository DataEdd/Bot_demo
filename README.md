## Inspiration
Have you ever walked out of a doctor’s appointment, already exhausted, only to be hit with a surprise bill? The expectation is endless phone calls, paperwork, and fighting with insurance companies just to understand what you owe. But what if it didn’t have to be that way? SHIPSmart is here to help UC students enrolled in SHIP take control of their healthcare costs. Our app estimates medical, dental, and vision costs upfront, ensuring the lowest possible price, and if our estimate is lower than what you were charged, we’ll fight for rebates and handle the follow-up claims. No more surprise bills, no more endless phone calls—just peace of mind knowing your insurance is working for you.

## What it does
SHIPSmart is a smart assistant for UC SHIP students, offering real-time cost estimates for medical, dental, and vision services.
Using a secure login system and a locally hosted database, SHIPSmart tracks user details, past visits, and insurance data, updating this info with each chat. When a user interacts with SHIPSmart, the AI gathers information about their symptoms, priorities, and insurance status. Based on this data, it searches our SQL database for the best available providers and streamlines the booking process, including extracting details from insurance cards to auto-fill forms.
SHIPSmart uses UC SHIP data to provide accurate medical cost estimates. By training an AI model on policy documents and using regression analysis on historical data, we guarantee precise estimates. Any discrepancies in pricing are flagged and managed — the AI will work with insurers and providers using Cerebras AI to track down the reason for the difference, ensuring users are either refunded or the issue is explained.
Additionally, SHIPSmart updates policy changes and healthcare charges in real-time, automatically analyzing data to identify trends and price fluctuations for specific procedures.

## How we built it
We designed the app's interface using Figma to create an intuitive, user-friendly experience. The frontend was implemented with SwiftUI, ensuring smooth performance and a native feel on iOS devices.
To power the user-facing side, we utilized the OpenAI/Gemini framework to build a complex AI agent that interacts with users, gathers necessary medical and insurance details, and provides real-time estimates.
For backend functionalities, we integrated Cerebras AI to handle communications with insurers and providers, ensuring discrepancies in pricing are addressed. The AI also automates the filling of online intake forms by extracting relevant information from our database when possible.

## Challenges we ran into
First time we built a mobile app using swiftUI so it took us a lot of time to get used to the platform. Also, we had problem in calling API and apply Firebase framework in swiftUI. Our designer find it hard when it comes to design for a chatbot so she struggled in finding ideas and resources. More than that, we changed lots of idea and design to fit the app and it took us lots of time and effort. But fortunate, we finished half of the app and will build the app more in the feature. Data mining to fill the SQL databases with providers was unexpectedly difficult due to the unintuitive design of the Anthem website and the limited unstructured data we could collect was not suitable for our purpose so for our demo we exclusively used synthetic  data.

## Accomplishments that we're proud of
I have never done any project in swiftUI and none of us have experience in developing AI. But, we successfully integrated Cerebras API and can call the function to run the app. We aook advantage by using all the resources at HackDavis and workshops hosted. At the end of day, we created the ideal end-to-end flow where the AI not only predicts, but also closes the loop 
We also proud that we stayed positive and stayed all night for debugging and building because it is easy to give up but hard to stay on track.

## What we learned
We have learned about leadership, teamwork, equity, and etc. We shares ideas to each other and respected each other. We learned new programming language, skills in API calls and AI/ML data. 

## What's next for SHIPsmart
Expanding Coverage: We plan to broaden our reach to include all California residents, providing everyone with easy access to accurate cost estimates and insurance benefits.
Multi-Insurance Support: We'll add functionality to handle users with multiple insurance policies, ensuring that estimates are optimized across all available coverage.
Health Watchdog: We aim to introduce a passive health listener, which will monitor users' health activities and proactively recommend preventive care and services that are fully covered by their insurance, helping users get the most out of their benefits.