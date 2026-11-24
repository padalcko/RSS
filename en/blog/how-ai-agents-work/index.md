# Anatomy of an AI Agent: How AI Agents Really Work

Language: English

Canonical HTML page: https://raccoon-studio.com.ua/en/blog/how-ai-agents-work/

> Learn how AI agents work, what they are made of, why they make mistakes and how they automate business tasks. Explained by a developer in plain language.

AI and Automation

While developing automations and AI agents, I often meet people who do not quite understand how these systems work. Some think an agent is just a chatbot. Others see it as a digital employee who only needs to be given a task before delivering the expected result.

Oleksandr Padalko · 24/11/2026 · 16 min read

![Raccoon SEO Studio mascot explaining AI agent architecture and its connections to digital tools.](https://raccoon-studio.com.ua/images/blog/how-ai-agents-work-cover.webp)

I want to explain how these systems are built, why they make mistakes, what determines their operating costs and when a business actually needs an AI agent.

You do not need any programming knowledge to understand this article.

## What is an AI agent?

Imagine that you run an online store. Every Monday, you want to receive a spreadsheet containing the prices of your five main competitors through Telegram.

You can ask ChatGPT to perform such a task during a conversation. However, to perform it automatically on a regular basis, you need a system with access to the necessary tools, a schedule and a way to deliver the results.

Such a system could find competitor websites, examine their offers, collect information, compare prices, prepare a spreadsheet and send it to you.

The language model itself does not open a browser, create files on a disk or log in to Telegram. These operations are performed by the software connected to it.

The language model determines what needs to be done, while the software executes the corresponding action.

## What is an AI agent made of?

In simple terms, an agent consists of several main components:

- A large language model (LLM), such as GPT, Claude or Gemini.

- A software layer that manages the model.

- Tools for performing specific operations.

- Mechanisms for storing information.

- Rules, restrictions and result validation mechanisms.

Developers often refer to the software layer that manages the model as a harness.

It passes the task to the language model, receives requests to perform operations, runs the appropriate tools and returns their results.

For example, if an agent needs to find the current price of a product, the model can request the relevant webpage. The harness receives the request, downloads the page and passes its contents to the model.

The model then analyses the information and determines the next action.

This process may repeat many times within a single task.

## How does an agent use tools?

Imagine that I am developing an agent for competitor analysis.

I can provide it with the following tools:

- Internet search.

- Webpage content retrieval.

- Calculations.

- Spreadsheet creation.

- Telegram messaging.

Each tool has a specific purpose, a description and parameters required to run it.

When the model determines that it needs to find competitors, it uses the search tool. After receiving a list of websites, it retrieves their content. Once the information has been collected, it can move on to preparing a spreadsheet.

This mechanism is known as tool calling.

The developer determines which tools are available to the agent. The model decides when and why to use them within the capabilities it has been given.

If I do not provide the agent with access to email, it cannot read my messages through an email tool. If I do not connect Telegram, it cannot send messages there.

An agent's capabilities depend largely on how it has been designed.

## What is MCP and why is it useful?

When developing agents, we often need to connect them to external services. These may include Google Drive, Gmail, CRM systems, GitHub, databases or internal business applications.

In 2024, Anthropic introduced an open protocol called MCP, or Model Context Protocol, to simplify these integrations.

It can be compared to a universal USB-C connector.

Instead of creating a separate communication mechanism between an agent and every external system, developers can use a standardised protocol.

For example, an MCP server for email could provide operations for searching messages, reading their contents or creating drafts.

The agent receives information about the available operations and can use them while performing tasks.

However, MCP does not replace authorisation, remove the need to configure access permissions or guarantee security on its own.

It provides a standard way for AI systems to communicate with external tools.

## How is an AI agent different from conventional automation?

Imagine that your website has a contact form. Whenever a customer submits it, the information should be saved in your CRM, and a manager should receive a Telegram notification.

Artificial intelligence is not necessary for this.

You can create a simple automation in [n8n](https://raccoon-studio.com.ua/en/blog/how-to-build-ai-agent-n8n/) that receives the data, validates it, saves it in the CRM and sends a notification.

The sequence of operations is known in advance. The result of each step can be checked using conventional code.

The situation changes when you need to analyse the customer's enquiry, identify their needs, find a suitable service, prepare a personalised response and determine which specialist should receive the request.

Using a language model may be justified in this case.

If the system also needs to select information sources, tools and the sequence of actions depending on the situation, we can talk about an agentic approach.

In my work, I prefer combining conventional automation with artificial intelligence.

Where a result can be obtained using ordinary code, there is little reason to spend language model resources.

## Practical example: a morning email assistant

Imagine starting every working day by checking your email. During the night, messages arrive from customers, advertising newsletters, invoices, service notifications and ordinary spam.

Instead of spending time reviewing every message each morning, you can automate their initial analysis.

Every day at seven in the morning, the system connects to your mailbox, retrieves new messages from a defined overnight period, analyses their content, assigns categories and prepares a short report delivered through Telegram.

To build such a system, you can use n8n, an email connection, a language model and a Telegram bot.

### What does the n8n workflow look like?

![n8n automation workflow for morning email analysis and Telegram report delivery.](https://raccoon-studio.com.ua/images/blog/n8n-email-assistant-workflow.webp)

A simplified n8n workflow for an email assistant. The labels in the illustration are in Ukrainian.

The first node starts the automation every day at 07:00. The next node retrieves new messages from Gmail. The language model analyses their content, determines their category and importance. Conventional code counts the results and prepares a report, which the Telegram bot sends to the user.

The AI Agent node in the illustration represents the email analysis component. In an actual implementation, a language model must be connected to it. If independent tool selection is unnecessary, a standard LLM node or text classifier is sufficient.

### What does the user receive?

You wake up, pick up your phone and see that 24 new emails arrived overnight. Eleven are work-related, eight have been classified as spam, and five are subscriptions or newsletters.

In addition to these statistics, the system highlights important messages: a confirmed customer meeting, a supplier invoice approaching its payment deadline and a new enquiry from your website.

![Example morning Telegram report from an AI assistant summarising 24 incoming emails.](https://raccoon-studio.com.ua/images/blog/ai-email-assistant-telegram-report.webp)

An illustrative example of a morning report delivered through Telegram. The message shown is in Ukrainian.

Conventional automation handles scheduling, email retrieval, counting messages and sending the report. The language model analyses the content and determines the category and importance of each message.

The system only needs read access to the mailbox. There is no need to allow it to delete messages or reply on your behalf.

Its functionality can be expanded if necessary. For example, the assistant could prepare draft replies, identify invoices, extract task deadlines or suggest adding meetings to a calendar.

If the model can independently select the appropriate tools depending on the contents of a message, the automation begins to take on the characteristics of a fully fledged AI agent.

It is a relatively simple system that does not require complex architecture but could save time every day.

## Why an AI agent cannot always read a website

As a web developer and SEO specialist, I find this particularly relevant.

When a person opens a webpage, they see images, prices, buttons, product specifications and other elements.

An agent may receive completely different information.

Some modern websites load their data through JavaScript after the initial page has opened. If the agent's tool retrieves only the initial HTML, the required information may not be present.

A person sees the product price, while the agent receives an empty container.

A full browser, such as Chromium controlled through Playwright, can be used to handle such tasks.

There is also a technology known as Computer Use, which allows a model to analyse screenshots and generate instructions for clicking buttons, entering text or scrolling through a page.

These operations require more time and computing resources.

When developing an agent, it is important to choose the appropriate method of retrieving information. If the necessary data is available through an API or a conventional HTTP request, there is no need to launch a browser.

## Why AI agents forget their original task

If you have worked with ChatGPT or another language model in a long conversation, you may have noticed that it sometimes starts ignoring previous agreements.

You have already explained a particular requirement, but the model makes the same mistake again.

One reason is related to how the context window works.

The context window contains information provided to the model for its current task. This can include instructions, user messages, source code, search results, file contents and responses from external tools.

While an agent is working, the amount of this information continues to grow.

It opens one website, then another, reads documentation, runs several commands, encounters errors and attempts to fix them. All of this can accumulate in the context.

As the amount of information increases, the model may find it more difficult to identify important details and consistently follow the original requirements.

This phenomenon is often referred to as context rot.

Developers use various context management techniques when handling large tasks.

One of them is called compaction. The system creates a condensed summary of previous work to make room for new information.

An agent can also store intermediate results in separate files, databases or working notes.

Instructions for specific types of tasks can be stored separately and loaded only when needed. This approach is used by mechanisms such as Skills.

Important details may be lost during context compression. This is why critical operating rules should not exist solely as written instructions.

## Why I do not rely on a single prompt for agent security

Imagine that I am developing an agent for email management.

Its task is to identify unnecessary messages and prepare a list of emails that the user could delete.

I could write a system instruction explicitly prohibiting the agent from deleting messages independently.

But if its task is only to analyse email, why give it a deletion tool in the first place?

From an engineering perspective, restricting its permissions at the software level is more reliable.

If the agent has read-only access, a language model error cannot cause emails to be deleted through that tool.

If deletion is a required feature, a separate approval mechanism can be implemented. The agent prepares a list of messages, and the user confirms the operation.

The same applies to files, financial transactions, databases, website publishing and other important resources.

A prompt defines the desired behaviour of the model. Software defines the limits of its capabilities.

## What is prompt injection?

Another problem arises when an agent receives information from external sources.

Imagine that it is analysing a competitor's website. The website could contain text that, instead of providing product information, includes instructions directed at the language model itself.

If the system handles such data incorrectly, the model may interpret these instructions as part of its assigned task.

This type of attack is known as prompt injection.

A particularly dangerous situation occurs when an agent simultaneously has access to confidential information, reads untrusted external sources and can send data outside the system.

Researcher Simon Willison calls this combination the Lethal Trifecta.

The risks can be reduced through restricted permissions, tool isolation, validation of external requests and human approval of dangerous operations.

If I am developing an agent to monitor competitor prices, it does not need access to my personal email, financial documents or internal company correspondence.

The fewer unnecessary capabilities a system has, the easier it is to control.

## Why are subagents useful?

Complex tasks can be divided among multiple agents.

Returning to the example of analysing five competitors, instead of having one model examine all five websites sequentially, separate tasks could be assigned to five subagents.

Each subagent works with its own information source and returns its results to the main agent, which prepares the combined report.

This approach makes it possible to separate context, perform operations in parallel and, in some cases, improve the quality of the results.

However, creating a team of agents does not guarantee better performance.

Every subagent consumes language model resources. Tasks must also be assigned, results collected, validated and combined.

If a simple task can be performed by one agent or an ordinary script, creating a multi-agent system will only increase development complexity and costs.

## Why AI agents can be expensive to operate

When using a language model in a normal conversation, people do not always think about the amount of information being processed.

When developing agents, this becomes an important consideration.

Language models process information in units called tokens. When using an API, costs generally depend on the number of input and output tokens and the selected model.

Imagine that an agent has been asked to check five webpages.

Instead of going directly to those pages, it starts examining the entire website structure, downloading additional documents, analysing external materials, running repeated checks and correcting its own mistakes.

The user assigned one task, but the system performed dozens of operations.

Sometimes this is justified. In other cases, the agent consumes resources on activities that are not required to obtain the result.

This is why agent development should include limits on the number of steps, context size, retries and available tools.

Not every operation requires the most expensive language model either.

Simple tasks can be assigned to cheaper models, while formal checks can be performed using conventional code.

The cost of operating an agent depends not only on the price of the model but also on the architecture of the entire system.

## Can an AI agent be trusted completely?

Imagine that an agent performs its assigned task correctly in 80% of cases.

At first glance, this may seem like a reasonable result.

However, if the agent needs to prepare a weekly report, assuming independent executions, the probability of receiving four correct reports in a row is approximately 41%.

This is a hypothetical mathematical example, not a performance statistic for a particular agent.

If the system can detect errors and retry a task, its performance may improve.

However, repeating an operation does not always solve the problem. If the agent uses an incorrect information source or one of its tools is malfunctioning, it may repeat the same mistake.

It is therefore important not only to obtain a result but also to have a way of verifying its correctness.

Automated tests, code-based validation, additional models and human oversight can all be used for this purpose.

In AI development, such evaluation methods are often referred to as evals.

For example, if an agent needs to collect prices from five competitors, conventional code can verify the number of records, the presence of required fields and the validity of the data format.

However, verifying whether a particular price actually belongs to the correct product may require additional checks.

The level of verification should reflect the consequences of a potential error.

A mistake in an article draft and a mistake during a financial transaction have very different costs.

## A practical example from my work: Raccoon SEO Scanner

One of the areas I work on is the automation of technical SEO audits.

Such a task can be implemented using n8n, conventional code and a language model.

As part of the development of Raccoon SEO Scanner, I am working on a system that receives a webpage URL and checks:

- HTTP status.

- Title and Meta Description.

- H1 headings.

- Canonical.

- Robots directives.

- Hreflang.

- Open Graph.

- Images and their alternative text.

- Internal and external links.

Artificial intelligence is not necessary for most of these checks.

Conventional code can determine whether a page contains an H1 heading, which URL is specified in its canonical tag and which HTTP status the server returns.

Passing the entire HTML document to a language model and asking it to perform every check would be an unnecessary use of resources.

However, once the results have been collected, a language model can be used for a different task.

It can explain to the website owner what the detected issues mean, why they matter, which ones should be addressed first and what to do next.

Conventional code collects factual data, while artificial intelligence helps interpret it.

In my opinion, these combined solutions have considerable practical potential for businesses.

## Where should a business start with automation?

I would not recommend starting with the development of a universal AI agent that is supposed to do everything.

First, identify a specific process that regularly consumes your time or the time of your employees.

This could be handling enquiries, preparing reports, analysing documents, monitoring competitors, classifying customer requests or managing a customer database.

Then determine which operations can be automated using conventional code and where a language model is genuinely necessary.

For many tasks, n8n or Make will be sufficient. Others will require connecting a language model through an API. More complex processes may require a fully fledged agentic system.

The choice of technology should depend on the task, not on the popularity of a particular tool.

## My conclusions

I see AI agents as another tool available to developers. A powerful and promising one, but one with its own characteristics and limitations.

I enjoy building systems that can work with information, analyse it and perform operations that previously required hours of manual work.

At the same time, I see little reason to introduce artificial intelligence into every process simply because it is currently popular.

If a task can be solved with ten lines of JavaScript, I will use ten lines of JavaScript. If a large amount of unstructured information needs to be analysed, I will connect a language model. If a system needs to independently select tools and plan its actions, I will consider an agentic architecture.

For a business owner, the number of language models, subagents and tools operating inside the system is ultimately of little importance.

What matters is that the system performs its work correctly, saves time, does not create additional problems and costs less than the process it replaces.

In my opinion, that is where the development of any automation should begin.

## About the author

Oleksandr Padalko

Frontend Developer / SEO Engineer

Raccoon SEO Studio

Planning a new website or trying to understand why your existing site gets little organic traffic? Raccoon SEO Studio works with technical SEO, web development and website optimization.

[Studio services](https://raccoon-studio.com.ua/en/#services)
