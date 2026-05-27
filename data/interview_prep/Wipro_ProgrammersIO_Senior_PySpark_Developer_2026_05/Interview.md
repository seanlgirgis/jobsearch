

Hi, how are you?

Speaker 1   00:02
Good. How are you? I'm doing fine. Thank you, sir.

Switch on my camera of my. It won't allow me sensor connected to the client Network right now, but don't worry about it. It's not a problem at all.

Speaker 2   00:24
Uh

Speaker 1   00:25
Weekends, so thanks for your time for this interview. Can we start with about lawsuit about what we have done? Professional experience. Yes, I mean, I, I have long, you know?

Speaker 2   00:46
Work experience in the I.T. Started long ago from our CC plus plus Unix. You know? Ctrl M that was in in the Telecom industry, I, you know? Lately in my work and City, you know, I? I worked with. Uh, you know data pipelines and forecasting? Um, and stuff like that, and we started from working with you know, the the regular stack and?

And bison and SQL. When the um, the amount of uh of data became a lot larger, we moved to buy spark and Hadoop. Uh, in order to have distributed Computing for. You know for our data, so I, I have a broad experience, and I worked with, you know, different development techniques and and different languages for a long time now.

Speaker 1   01:54
Okay, uh, so can you tell me about the spark architecture?

Speaker 2   01:59
Yeah, well, I mean, when you talk about spark, one of the important things that it brings. It brings lazy execution basically so. You know and and in in spark, you know, different than the? Regular like, say, python, banders, you, you start, and? You know, you do any transformation or any work like that and and immediately it's it's at, uh?

It starts to execute that for you. However, when you go and Spark, you have a different concept you have, like drivers. The the driver basically takes your. Uh, you know, intented action ex the the Transformations? Uh, things that you want to do, but then it kind of planned them for you.

Then you would have, uh, to go after that, into kind of like a cluster management because you have more than one. You know? One note working. So, once you you have, you know, an action, an action something like, you know, account, or, you know, things of that nature? You know, you go into executors basically, and the executors would be executing your.

Uh, the the actions that you are requiring into the different cluster nodes. And then, uh, you know, uh, it Aggregates the the results and turn them back to you. Uh, which makes it a little different than working with straight programming expert built around, uh, in Java and? You from the point of view of python.

Use Pi spark to to work against it. You have also GUI and logs and things of that nature that he can use to. Uh, to work against it.

Speaker 1   04:05
Can you tell me like, what is, or in which cases would you use, uh, already, and in which case you would use a data frame? Well, R is more of, you know, the kind of, you know, under, under the hood and? Uh, it's much closer to.

Speaker 2   04:28
Uh, you know, the the interworkings of biaspark, uh, honestly. Most of the time, we use data frames because it's. That's more similar to the workings of, you know, what you would have with pandas and stuff like that?

Speaker 1   04:54
Have you worked on any Cloud systems? Yes, yes, we. We work with, uh, AWS. You know, touch it on. Um, the storage layer in S3 and. Uh, Lambda. We, we had. Uh, you know?

Speaker 2   05:17
Kubernetes. And glues offs and stuff like that.

Also in the spot. How can you award shuffling?

Speaker 1   05:33
Oh, avoid. I avoid

Speaker 2   05:36
Shuffling. Well, you know you. You have an issue with shuffling. Shuffling is, uh, is pretty costly, so? If first of all you know good good partitioning and good planning, uh, I mean, would not 100 percent avoid shuffling, but would reduce the possibility of shuffling, but however, if you are with a smaller data set.

And you want to join it. Sometimes, if you use broadcasting, that might help a lot, you know, for reducing the amount of? Uh, you know of of waste and processing by broadcasting the small set. If you have a small enough set, and then you have multiple partitions, then you can broadcast that set onto the partitions, and you do the joins in there and then, you know.

Does the the, uh? The growing on the differences and brings everything back that sometimes you know would really. But all the, because if you are having a big set against big sets, you might. It might be a lot harder, so it's more. It could be more of a blinding, so broadcasting is is one of the keys that he can use to reduce shuffling.

Shuffling is a big deal, and it costs a lot of, you know, processing. And waste. Okay, um, what are some other methods which can help to improve performance? Um.

Yeah, performance in spark is is a big issue, and it's, it's a great questions, but sometimes you have to take it from the the planning side. Uh, from, you know, top down, you have to, uh? You know, check the the the you, the joints that you have, and you have to make sure that you are not also.

Uh, doing repeated actions, because each action that you do would would result on students. So, uh, there are multiple things that you you got to do to look at, you know, the performance? So, so the kind of joints that you are using the the numbers of actions that you are using, you know?

Are you hitting shuffling? Are you doing correct partitioning to begin with? Efficient partitioning would help a lot in the performance of your buy spark. Um, can you tell me, uh, what is the Adaptive query notion? Adaptive query resolution.

No, actually, I'm honestly I didn't. Um, so in Facebook, let's say. Um, I have a table all right.

Speaker 1   08:42
And I want to fetch the second highest salary of. On the top 10 salary salary employees as per like our department. So, for example, there are three or four departments, and I want to find out the doctor seller replacing each department? So, how would I build the logic to find the top two salaries salary deliveries?

Bird Department.

Speaker 2   09:14
Okay. Well, the the one of the things that he can do is you can work with. Let's say with when doing, you can create Windows and you can sort each window and you can take the up two of each one of them.

Speaker 1   09:40
Ways, as you can use Windows,

Speaker 2   09:44
You can, and, and you can. You know, use it to pocket the data, and then you can sort on each window on the salary descending, and you can take the top.

Speaker 1   10:02
So, like, what would be your syntax of in your Pi spark command? Oh, you want the exact syntax right now. Yeah, like, more function, or what function only use?

Speaker 2   10:19
Uh, you were, you would do partition buy on the the department. And you can order by the salary descending. Okay, and then you can take the top to limit for the two. All right.

So?

Speaker 1   10:48
What is the difference between a group by key and reduced by key and which one is beneficial to use?

Speaker 2   11:02
Um, I, I, you know, I, I have used Group by, but I haven't used much reduced by actually tell you the truth. Okay, okay. Well, but but, you know, like, what will be the difference or any idea? No, honestly, not much. Okay, okay.

Speaker 1   11:24
Hmm.

Okay, so if you have to schedule the task? Um, so how would you achieve that? To run in spark engine. You know, I mean, uh?

Speaker 2   11:51
The, the, the best thing is to use schedulers. And, you know, the main airflow comes to mind. This is kind of like the main Apache airflow is one of the main ones, and it gives you the ability to get asked since you have dependencies. And, uh. It creates it as if it's a dag.

So, so? It gives you lots of abilities and also to enable you to schedule tasks across multiple applications. Also, control M and autoss are two other systems that you can use to work on on scheduling tasks. Okay. Okay.

Speaker 1   12:33
Then tell me, what is the difference difference between repartition and polish? Between the repartition and what? A police. Oh, cool, s okay.

Speaker 2   12:50
You know, I? I haven't used Coles a lot, but uh, repartitioning is usually is, is, is a lot exp. It's an expensive task to do because it causes lots of shuffling of data between partitions and stuff like that. So, you have to be very, very careful when using them.

Okay. Um, so you have, like, how much money rate yourself in? The school de la place? I, I do very well with SQL queries, you know. I, uh. Uh, I, I, you know, worked with whole variety of advanced queries from, you know, uh? When doing two case statements and stuff like that?

Okay, so the example that I was talking about earlier right to find the?

Speaker 1   13:42
So, talk to yes, sir employees, uh, do that through my SQL playing. Um. Well, you can do. In SQL query you, you can do.

Speaker 2   14:02
So, let's go back again. Can you explain again the the scenario that? So I, I have a several employees working in each department. I want to find the top two seniorate employees, uh, in each department. So, how would you form a SQL query for that? Uh, one one way you can use.

Uh, CTE. Queries, and you can, which basically you can join them together. So, each one you can do for each department and you can order the. You can order the the employees for each department, and you can take limit two for each, and you do Union for those so you can get the the group of employees.

Like, you know, if you want the top two for each department, so you know, uh, it's CTE, makes a makes coding a lot easier? Because basically it creates as if virtual table for each. So, if you filter for bird Department? I, I mean, uh, and you can add them together.

You can join them together. So, so this is one of the the ways. Uh, that you can do that. Or you can, do you know? Again, you can do the the window idea, but you can you. You can partition by the department. Id itself. And then you can order by the salary and you take the top two for each.

Okay.

Speaker 1   15:46
Apart from partition by and order ordering by the salary. Anything else you would use, like, how would you find out the top two? To finding the.

Speaker 2   15:59
The top. That's any other function. These are kind of like the two that comes to mind actually. Okay, okay, uh?

Uh, you have worked on Sanscripting as well. Yes, sir. Yes, sir. Okay, okay.

Speaker 1   16:24
Now, let's say I want to. I want to pray people, maybe several lines in a while. Yes, sir, and I want to print. Line number, let's say, from 15 to 20. Okay, I'm fine. So, how can I do that?



To.

Speaker 1   00:01
From the file.

I, I know that you can. You can tail and and say, you can use head or tail to get the top number of records or the latest number of Records, but exactly, I, you know, the the line 15 to 20, I haven't. I haven't done that for a while.

Okay, okay, that's fine, um, right? Coming back to spark, um?

Speaker 2   00:36
There are different kind of. Um, storage. Level three. Uh, can you tell me about those?

Of persistence levels in a spark.

Speaker 1   00:51
Storage levels, something like hdfs and stuff like that, or what? What do you mean by

Speaker 2   00:57
It? No, no, no, so, uh, techniques right in the spark? Aha, aha. Well, can you tell me about those? What are the different types of persistence levels, uh, available? Uh, honestly, I, I don't know. Okay, okay. Um.

Speaker 1   01:31
Do you know about the predicate pushdown? Predicate. Who's down? Predicate push down. Bush down or breath. Get push down. No, no. Okay, okay.

Speaker 3   02:02
So, uh, in which case would you use a broadcast join?

Speaker 1   02:07
Uh, you you use broadcast join if you have a smaller set that you want to join with. You know, compared to what you have in your different partitions? Uh, when you do broadcast join, that will prevent it from doing lots of shuffling basically. At broadcast, a small set to the different partitions does the joining end, and then bring everything back.

Okay. Okay, um?

Speaker 2   02:39
So, do you know about, like, if the, for example, there is skewed data? Okay. Uh, how can we? To fix that. Install what type of techniques are available with us to help fix skewed data? Can you elaborate on on? You know, what do you mean by that? So, we, like, a.

This is a kind of, uh, let's say. So, we are running into. Performance issues? Yes. Okay, um? And. Still detangle sense of the cluster is like? Oh, more, heavily used for a particular partition.

Speaker 1   03:29
Yes, so how can we try to, you know, avoid that, uh? Or how can we try to improve the performance, uh? Of the cluster. Yes, I mean that that can happen and and what we need to do. We have to find out what is the problem with the skewed data?

Uh, basically, you you have to investigate your data and see. Say, the the amount of nulls that coming in the types of joints that you have because some joints that might not be done very carefully that would result in massive amount of data. Uh, so, and also you have to look at the way the partitioning happened.

Like, say, if you are working say with with? Data that's heavily based on dates, basically, and stuff like that. So, you have to look, how are you? Are you partitioning the the data correctly, so the the data would would be joined in different like, you know, partitions, and stuff like that.

So, basically, the uh, are your partitions? You know, or you are trying to partition. And it's like, uh, so many partitions that causing fragmentation that causing the the the the queries to be very slow, so you increase, you know, uh, there's kind of The Sweet Spot between, like, being over fragmented or?

It is like, you know, uh, partitioned correctly, so? There's lots of procedures and things that you need to work on to improve on the, uh, you know, performance of your queries basically. Okay, um?

Do you know about salty? About WhatsApp. Sorting.

Speaker 2   05:34
Yeah, yes, s, a, l, t, i, n, g, no salting, I understand, yeah, salting, no. Okay, um? Okay. For example, there is an array, okay, and uh, and I want to flatten the elements in the array. Using principal. So, how can I do that?

You want to flatten the array?

Speaker 1   06:05
But I don't know. Okay.

For. For

Speaker 2   06:17
Example, there are two arrays. Okay, yes.

Speaker 1   06:20
And I want to find out the common elements about the arrays. Okay, so what function I can use to find that out?

Speaker 2   06:31
And and buy spark.

Speaker 1   06:42
You want to get the the common items you? You can use an inner join in that join, and that, and basically, that will give you the common items between the two set of records that you have.

Speaker 2   07:00
Okay, so in Paiser, can you tell me like, what will be the, uh, joint syntax?

Speaker 1   07:07
You want the the joint syntax, and that if you, if you're not join. For example, if you want to join two data frames. Okay, okay. So, what would be your drawing syntax? You, you would have, you know? A group of like, you know, left, set, and say, right, set, or whatever, or set one set to use join and you, you tell it, which field you are joining on and and you tell it the type of join, which will be enter?

Like, for in the drawing. Okay, okay, all right. Um, okay, I'm good, Sean. Thank you, sir. Yeah, do you have any questions for me? Yeah, I mean. What, like, you know for? For the the project is this particular project that you are guys hiring for, or is this, you know, a shop that works with multiple projects and stuff like that?

Like, are you working say was financials? Yeah, so mostly it will be Financial cost, um?

Speaker 2   08:17
Hassan, but I am not part of the project. I am in a different project. Oh, but this hiring is for another project. Oh, for another project.

Speaker 1   08:26
Great, great! Thank you very much. And what's the hiring process goes from here?

Speaker 2   08:33
Perfect!

Perfect, perfect! Thank you very much has been pleasure talking to you.
