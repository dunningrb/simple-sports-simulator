## Simple Sports Simulator.
A Python package for simple simulations of various sports leagues.
This is a toy project I created for fun.

#### Basic Idea

The Simple Sports Simulator simulates matches between competitors
in various sports leagues, such as soccer (association football),
basketball, baseball, and hockey. I'm working on adding chess.

The simulation is best explained through an example. Suppose we
want to simulate a match in the English Premier League between 
Chelsea and Manchester City. The simulation model requires some
input data, which we can pull from the current EPL season (or any
past season, or we can just make up the numbers):

    Manchester City:
      avg_shots_for: 16.32
      goal_pct_for: 0.115808824
      avg_shots_against: 7.53
      goal_pct_against: 0.120535714

    Chelsea:
      avg_shots_for: 13.85
      goal_pct_for: 0.119133574
      avg_shots_against: 9.75
      goal_pct_against: 0.117948718

            * avg_shots_for: the average number of shots the team takes in one game
            * goal_pct_for: the percentage of the teams's shots that score a goal
            * avg_shots_against: the average number of shots the team's opponent takes in one game
            * goal_pct_against: the percentage of the opponent's shots that score a goal.

In addition to the values for each team, the simulation model needs
the corresponding values for the league:

    English Premier League:
      avg_shots: 11.913
      goal_pct: 0.11516

            * avg_shots: the average number of shots taken by one team in one game
            * goal_pct: the percentage of all shots that score a goal

Manchester City averages 16.32 shots per game. This is well above the league
average (11.913). But Chelsea allows only 9.75 shots per game, which is below 
the league average. So how many shots do we expect Manchester City to take in
a match against Chelsea?

We calculate the value from

    (EPL avg) + (Man City avg + Chelsea avg - 2 * EPL avg) / sqrt(2)

    11.913 + (16.32 + 9.75 - 2 * 11.913) / sqrt(2) = 13.5

Chelsea's expected number of shots is

    (EPL avg) + (Chelsea avg + Man City avg - 2 * EPL avg) / sqrt(2)

    11.913 + (13.85 + 7.53 - 2 * 11.913) / sqrt(2) = 10.2

A team can take only an integer number of shots, so each of these values is
converted to the nearest integer. Additionally, we model home field advantage
by adding a constant (across all league matches) value to the home team's
number of shots and subtracting it from the away team's number of shots. If
Chelsea is the home team, the number of shots for each side will be

    Manchester City..... int(13.5) - 1 = 13
    Chelea.............. int(10.2) + 1 = 11

Next we calculate each team's goal percentage. Manchester City's goal
percentage against the entire league is 0.11581, while Chelsea permits
a goal percentage of 0.11795 against the entire league. The league goal
percentage is 0.11516. We combine these numbers in the same formula to
determine Manchester City's goal percentage against Chelsea:

    (EPL avg) + (Man City avg + Chelsea avg - 2 * EPL avg) / sqrt(2)

    0.11516  + (0.11581 + 0.11795 - 2 * 0.11516) / sqrt (2) = 0.11759

For Chelsea:

    (EPL avg) + (Chelsea avg + Man City avg - 2 * EPL avg) / sqrt(2)

    0.11516  + (0.11795 + 0.12053 - 2 * 0.11516) / sqrt (2) = 0.12093

So, Chelsea will take fewer shots than Man City (11 to 13), but will have a
slightly higher probability of scoring on each shot (0.12093 to 0.11759).

To determine the final score and outcome of the game, we generate a
sequence of random numbers between 0 and 1 and compare each to the teams'
goal percentages. Since the model is not simulating the internal dynamics
of a football match, we just imagine Man City taking 13 consecutive shots
and Chelsea taking 11 consecutive shots. (Each "shot" is the random number.)

    MAN CITY SHOTS
        Shot #      Random      Less than 0.11759?      Goal?
        -----------------------------------------------------------------
            1       0.836351        No                  No
            2       0.268326        No                  No
            3       0.855459        No                  No
            4       0.101949        Yes                 YES
            5       0.601754        No                  No
            6       0.091847        Yes                 YES
            7       0.387062        No                  No
            8       0.009084        Yes                 YES
            9       0.594769        No                  No
            10      0.362359        No                  No
            11      0.311933        No                  No
            12      0.628280        No                  No
            13      0.553934        No                  No  (3 goals)

    CHELSEA SHOTS
        Shot #      Random      Less than 0.12093?      Goal?
        -----------------------------------------------------------------
            1       0.295288        No                  No
            2       0.915525        No                  No
            3       0.692082        No                  No
            4       0.936151        No                  No
            5       0.452980        No                  No
            6       0.222099        No                  No
            7       0.342133        No                  No
            8       0.688582        No                  No
            9       0.208902        No                  No
            10      0.479790        No                  No
            11      0.065601        Yes                 YES (1 goal)

Manchester City wins this simulated match 3-1.

Hockey is simulated in an identical way. The basketball simulation is
essentially the same, except it distinguishes between free throws (1 
point each), ordinary field goals (2 points each), and three-pointers
(3 points each) to accumulate a team's final score.

The baseball model is fundamentally different. It's based on a variety
of dice games and old board games that simulated a complete game in a
few rolls. That particular model does not work very well. It's closer to
wiffle ball than baseball. Improvements are in the works.

The chess model will be based entire on ELO ratings, and for a given
match will determine the winner, loser, or a draw.

#### Simulating a League

To simulate a league requires a YAML file with input values for the
league averages and for the individual teams. In all cases, in the
current version of the code, each team in the league plays the other
teams once per round, with home field alternating between rounds. I.e.,
there are no divisions or conferences.

Some example YAML files are available in the repo.

#### Example Simulation

As an example simulation, consider 