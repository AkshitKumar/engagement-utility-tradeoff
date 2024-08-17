import numpy as np
import matplotlib.pyplot as plt
from helper import *
from parameters import *

def simulate_dice_given_niche(popular_base_utility, outside_base_utility, niche_base_utility, delta, N, num_sim, tau):

    # look at the first tau periods (exploration phase)
    outside_option_exploration = outside_base_utility + zero_mean_gumbel(num_sim, tau)
    popular_option_exploration = popular_base_utility + zero_mean_gumbel(num_sim, tau)
    niche_option_exploration = niche_base_utility + zero_mean_gumbel(num_sim, tau)

    chosen_option_exploration = np.argmax(np.stack([outside_option_exploration, popular_option_exploration, niche_option_exploration], axis=2), axis=2)
    # count the number of times each option is chosen in each simulation
    num_outside_pick = np.sum(chosen_option_exploration == 0, axis=1)
    num_popular_pick = np.sum(chosen_option_exploration == 1, axis=1)
    num_niche_pick = np.sum(chosen_option_exploration == 2, axis=1)

    # find rows where num_niche_pick is more than num_popular_pick
    idx = num_niche_pick > num_popular_pick

    # number of times the niche option is chosen more than the popular option
    num_niche_picked_more = np.sum(idx)
    user_choice_exploration = chosen_option_exploration > 0
    user_utility_exploration = np.maximum( outside_option_exploration, np.maximum(popular_option_exploration, niche_option_exploration))
    engagement_vec_exploration = np.sum(user_choice_exploration * delta ** np.arange(tau), axis=1)
    utility_vec_exploration = np.sum(user_utility_exploration * delta ** np.arange(tau), axis=1)

    # look at the remaining N - tau periods (exploitation phase)
    # recommending both options of the popular type
    outside_option_popular = outside_base_utility + zero_mean_gumbel(num_sim - num_niche_picked_more, N - tau)
    popular_option_first = popular_base_utility + zero_mean_gumbel(num_sim - num_niche_picked_more, N - tau)
    popular_option_second = popular_base_utility + zero_mean_gumbel(num_sim - num_niche_picked_more, N - tau)
    popular_option = np.maximum(popular_option_first, popular_option_second)
    user_choice_popular_exploitation = popular_option > outside_option_popular
    user_utility_popular_exploitation = np.maximum(outside_option_popular, popular_option)
    engagement_vec_popular_exploitation = np.sum(user_choice_popular_exploitation * delta ** np.arange(tau, N), axis=1)
    utility_vec_popular_exploitation = np.sum(user_utility_popular_exploitation * delta ** np.arange(tau, N), axis=1)

    # recommending both options of the niche type
    outside_option_niche = outside_base_utility + zero_mean_gumbel(num_niche_picked_more, N - tau)
    niche_option_first = niche_base_utility + zero_mean_gumbel(num_niche_picked_more, N - tau)
    niche_option_second = niche_base_utility + zero_mean_gumbel(num_niche_picked_more, N - tau)
    niche_option = np.maximum(niche_option_first, niche_option_second)
    user_choice_niche_exploitation = niche_option > outside_option_niche
    user_utility_niche_exploitation = np.maximum(outside_option_niche, niche_option)
    engagement_vec_niche_exploitation = np.sum(user_choice_niche_exploitation * delta ** np.arange(tau, N), axis=1)
    utility_vec_niche_exploitation = np.sum(user_utility_niche_exploitation * delta ** np.arange(tau, N), axis=1)
    
    engagement_vec_popular = engagement_vec_exploration[np.where(idx == 0)[0]] + engagement_vec_popular_exploitation
    utility_vec_popular = utility_vec_exploration[np.where(idx == 0)[0]] + utility_vec_popular_exploitation
    engagement_vec_niche = engagement_vec_exploration[np.where(idx == 1)[0]] + engagement_vec_niche_exploitation
    utility_vec_niche = utility_vec_exploration[np.where(idx == 1)[0]] + utility_vec_niche_exploitation

    engagement_vec = np.concatenate((engagement_vec_popular, engagement_vec_niche))
    utility_vec = np.concatenate((utility_vec_popular, utility_vec_niche))

    engagement = np.mean(engagement_vec) * (1 - delta)
    utility = np.mean(utility_vec) * (1 - delta)
    return engagement, utility


def simulate_dice(popular_base_utility, outside_base_utility, delta, N, num_sim, num_samples):
    engagement_vec = []
    utility_vec = []
    niche_base_utility_vec = sample_gpd(mu, sigma, xi, num_samples)
    count = 0
    for niche_base_utility in niche_base_utility_vec:
        count += 1
        print(count)
        print(niche_base_utility)
        engagement, utility = simulate_dice_given_niche(popular_base_utility, outside_base_utility, niche_base_utility, delta, N, num_sim, tau)
        engagement_vec.append(engagement)
        utility_vec.append(utility)
    engagement = np.mean(np.array(engagement_vec))
    utility = np.mean(np.array(utility_vec))
    return engagement, utility