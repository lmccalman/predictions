# Christmas Predictions

## Background

The idea of predictions came about around the same time Trump was first rising
to power. A group of us were concerned that if this were a possibility, then
who knew what else the next year could bring.

To take part in predictions, each person puts forward a number of statements
that can be verified as true or false by the end of the year. These events
can occur earlier than the end of the year, but we need to be able to make
a call on them by that point.

Once we have collated the statements, each person assigns every statement
(theirs and other players') a probability: how likely they think the statement
is to come true.

Then, on Christmas Eve, we'll review all of the events, score everyone's
predictions, and declare a winner.

The scoring approach judges two aspects of our predictions:

1. How much knowledge each person has about the future
2. How accurately each person characterises their own level of knowledge

The second condition is important because it's required to make risk-based
decisions. Consider the question of whether it is safe to drive a truck over an
old bridge. If the probability of the bridge collapsing is say 47%, then the
bridge is still more likely to hold than not. If asked to predict 'will the
bridge collapse' as a yes-or-no question, a sensible expert would say no.
However, would you drive the truck over the bridge?

## The process

1. Early Jan: Everyone comes up with 5 statements
2. Mid Jan: Statements must be submitted (without probabilities) by
   a mutually-agreed date. These will be collated and a spreadsheet sent out
   to everyone with all the statements.
3. Late Jan: Everyone works on assigning probabilities to all the predictions
4. End Jan: Probabilities due for submission on a mutually-agreed date
5. Through the year: The Signal chat is active with discussion of statements as
   they resolve or don't
6. 15 Dec: The last date for predictions to be resolved, to give the
   game-runners some time to collate results
7. Christmas Eve: Winner announced!

## Coming up with statements

- Statements must resolve as true or false:
    Yes: The pope dies
    No: Predict the total number of popes in 2026

- Statements can't be 'personal', or directly relate to players
    Yes: predictions about famous people
    No: Andrew will shave his head

- It should be clear how to *measure* the truth of a statement, with as little
  judgement as practical:
    Yes: An earthquake in Japan will be measured with Magnitude 9
    Yes: The Guardian will report that Taiwan has been "invaded" by China.
    No: There will be a catastrophic earthquake in Japan
    No: China will attack Taiwan

## Resolving statements

Statements are generally resolved by consensus, though the CEO (currently
Bruce) has final say. When the truth of a statement turns out to be ambiguous
or players interpreted it differently when assigning probabilities, it may be
'zeroed-out' (not counted in the scoring).

## Scoring

The scoring for the game is *standardised log-likelihood* with respect to the
distribution defined by each player. The following section tries to justify and
explain why we use that, and what it means.

### Motivation

The scoring system in this prediction game tries to address both the quality of
a prediction (did it come true) and whether the level of certainty someone has
is appropriate to their level of knowledge.

The foundational idea is that for predictions to be useful, they have to have
a probability associated with them. An expert saying 'there's a 47% chance the
bridge will fail' is a useful prediction, because it allows for risk-based
decision-making. The difference between 47% chance of collapse and 0.000000047%
chance of collapse is critical, even if both would be summarised as 'the bridge
won't fall down' when made by a pundit.

But how do you assess the quality of a probability estimate? This is especially
difficult when it's impossible to know the 'true' probability: usually we just
know if, for example, the bridge held up or not when it was driven over.

The simplest way is to assess the quality of a set of predictions over a number
of different events. By looking at a number of events, we can see if someone is
overconfident in their predictions, under-confident, or 'calibrated', meaning
they correctly assess their level of knowledge.

Imagine we look at 10 events predicted by a number of different people:

- **Person A** assigned 99% to 5 events that happened, and 5 events that didn't. This person is over-confident: they got things wrong they were sure about
- **Person B** assigned 99% to 5 events that happened, and 50% to 5 events, 3 of which happened. This person is well calibrated. When they were confident they were right, and the things they considered toss-ups were that: about half of them actually happened.
- **Person C** assigned 50% to 10 events, 5 of which happened. This person is also well calibrated, though less knowledgeable than Person B.
- **Person D** assigned 99% to 10 events, all of which happened. This person is both well calibrated and extremely knowledgeable.
- **Person E** assigned 51% to 5 events all of which happened, and 49% to 5 events, none of which happened. Person E is under-confident: they knew the answers and so could have assigned higher probabilities to their outcomes.

Under-confidence is useless, but overconfidence is dangerous. There are
a plethora of pundits making predictions about what will happen in the future,
but these pundits are never asked to assign confidence to their predictions,
and are never judged based on the calibration of that confidence. The scoring
used in the prediction game is one way to judge the quality of punditry.

### Deriving a scoring system

What we want is a way to score predictions with the property that the maximum
attainable score corresponds to knowing the true probabilities of all the
outcomes. There are some deep questions about what a 'true' probability is, but
let's leave that aside for a moment.

In simple terms, we have a number of biased coins (that is, they don't land
heads or tails 50% of the time, but rather some unknown % of the time that
varies with each throw). The goal of the prediction game is to predict that
bias on the coin. We want a scoring system such that, if someone correctly
guesses the bias of every coin, they obtain the maximum possible score. Scoring
systems with this property are known as 'proper losses'.

There's another problem though -- we never actually observe the true bias of
the coins, we only get to toss them once and record the result. It turns out
that this isn't a deal breaker. Whilst it's possible for someone to get lucky,
if there are quite a number of coins to toss then we can construct a scoring
system in which it is extremely likely that the person who correctly guesses
the true bias of all the coins will get the highest score.

### Likelihood

One 'proper loss' is the *likelihood*. It works like this: We treat every
person's set of prediction probabilities as a model of the world, in other
words, we assume that they are the real probabilities of all the events. Then
we ask:

"How likely are we to have observed all the measured outcomes in each person's
model of the world?"

For example, given two statements:

Event A. Trump becomes God-emperor
Event B. The Queen is welded into a life-support throne

Let's say I assigned 0.8 to the first event and 0.9 to the second event. I've
implicitly assigned 0.2 to the first event NOT happening and 0.1 to the second
event NOT happening. This is just because probabilities have to sum to 1 over
the set of possible events (and for a true/false prediction, the set of
possible events is just 'does happen' or 'doesn't happen').

Say that the first event happens, but the second does not. Then my likelihood
score is:

Likelihood = P(A and NOT B)
 = P(A) * P(NOT B)
 = 0.8 * 0.1
 = 0.08.

Though it's possible to get lucky for a single event or two, over time, the
model of the world which captures the *TRUE* probabilities of events will always
have the highest likelihood score.


Another important thing to note about likelihoods of multiple events: If ANY
one of my probabilities for any event is 0, then my total likelihood will be
zero NO MATTER WHAT my other probabilities are, this is because 0 * X is 0 for
all X. 

#### Note on independence assumption
You may notice that substituting P(A) * P(NOT B) for P(A and NOT B) requires
assuming that these events are *independent*. For two independent events,
knowing the outcome of one tells us nothing about the probability of the other.
Most statements made in this game are NOT independent, however. 

To model non-independent events, we must assign probabilities to all
*combinations* of events, still while respecting the idea that all possibilities
must sum up to one. For the example above, this could look like the following
table:

A and B: 0.8
A and NOT B 0.05
NOT A and B: 0.05
NOT A and NOT B: 0.1

Then the likelihood would be 

Likelihood = P(A and NOT B)
    = 0.05

Players may, OPTIONALLY, choose groups of events over which to define these
kind of combinatorial probabilities. However, note a couple of things:

- it's really, really optional: No-one has ever done it, even Bruce
- Events can only be in one group: if you combine event A with event B, you
  can't also, separately combine event A with event C.

### Log-likelihood

Likelihood is the basis of the game's scoring, but by itself has 2 
problems.

1. For dozens of predictions, the likelihood score will be really, really small
   because we're multiplying lots of numbers less than one together.

2. The number is difficult to interpret.

To solve problem 1, we take the log of the likelihood. This transformation
doesn't affect the game, in the sense that players ordered by likelihood score
will maintain that ordering when ordered by log-likelihood. This transformation
has the advantage of making the numbers much more sensibly sized, but it also
turns the multiplication into an addition:

Likelihood = P(A)*P(B)
Log-Likelihood = Log(P(A)) + Log(P(B))

Now we can compute a score for each prediction and just add them up! We
previously showed that a single probability 0 in the likelihood means the total
likelihood will be zero regardless of probabilities for other events. The
log-likelihood maintains this same property because log(0) = negative infinity,
which always remains negative infinity regardless of what gets added to it.

For those interested, the log-likelihood also has the property of measuring the
(negative) self-information, "surprisal" or Shannon information for the event
under the provided probability distribution. For this reason, we use base-2
logarithms so that this quantity is measured in bits.

The "Surprisal" interpretation also provides some intuition for why the
log-likelihood is bounded above (ie there's a max score) but not below (ie you
can get negative infinity). Seeing an event with probability 1 occur isn't
surprising at all, but seeing an event with probability 0 occur is *infinitely*
surprising.

### Standardised log-likelihood

Logs are also pretty arbitrary numbers. (What does a score of -1.2 mean?) To
address this, we *standardise* the score of each prediction by subtracting the
score that a "naive" prediction would get: Here a naive prediction is the one
that implies no knowledge about the outcome, P = 0.5. So then for each
prediction:

Standardised-log-likelihood = Log(P(A)) - Log(0.5)

This means that scores above zero imply you've done better than someone
guessing 0.5, and scores below zero imply the opposite.

## Advice for coming up with good statements

The unstated secondary purpose of the game is to encourage players to engage
with each other's interests. So don't be afraid to make a prediction in an
obscure field that you have interest in -- hopefully other players will do some
research.

The most interesting statements have reasonable uncertainty: avoid things that
are extremely certain to occur or to not occur.


## Advice for assigning probabilities

For each prediction, the minimum possible score is negative infinity. The
maximum possible score is 1.

If you assign 0 probability to an event and it does happen, the data can
never be produced by your model and you will automatically get an overall score
for the year of negative infinity. It doesn't matter how good your other
predictions are. This is asymmetric -- if you assign 1 to an event and it does
happen, you get 1 added to your score, you don't automatically win.

If you guess perfectly and assign probability 1 to every event that occurs and
probability 0 to every event that doesn't occur, you will get a score equal to
the number of predictions. However, you can see how risky that strategy is.

Let's say you think Biden will win the next election. What probability do you
assign? One way to think about it is to imagine you had 10 unrelated questions
but about which you had a similar level of confidence. If you would expect to
be right about 8 of those 10 questions, then you should assign them all
a probability of 80%. This approach will maximise your score, given your level
of confidence is actually accurate (we call this being 'calibrated'). If you
were 'overconfident', that is, you assign very high or very low probabilities
to everything, then you'll get some things wrong that you assigned a high
probability to -- this causes your score to drop. On the other hand, if you are
'under-confident' and say, put everything as a 50-50 chance, then you've left
money on the table -- you could have used your predictive power to increase
your score by assigning more probability to correct outcomes.

- If you have no idea, put 0.5
- If you are sure, don't put 1 but something close to 1
