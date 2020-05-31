

#
db.getCollection('test_stats').aggregate([
{$match: {}},
{$group: {_id: "$genome_id", total: {$sum: "$1_comprehended"}}}

])


# Exposed vs. comprehended numbers
﻿db.getCollection('test_stats').aggregate([
{$match: {}},
{$group: {_id: "$genome_id",    total_exposed_0: {$sum: "$0_exposed"}, total_comprehended_0: {$sum: "$0_comprehended"},
                                total_exposed_1: {$sum: "$1_exposed"}, total_comprehended_1: {$sum: "$1_comprehended"},
                                total_exposed_2: {$sum: "$2_exposed"}, total_comprehended_2: {$sum: "$2_comprehended"},
                                total_exposed_3: {$sum: "$3_exposed"}, total_comprehended_3: {$sum: "$3_comprehended"},
                                total_exposed_4: {$sum: "$4_exposed"}, total_comprehended_4: {$sum: "$4_comprehended"},
                                total_exposed_5: {$sum: "$5_exposed"}, total_comprehended_5: {$sum: "$5_comprehended"},
                                total_exposed_6: {$sum: "$6_exposed"}, total_comprehended_6: {$sum: "$6_comprehended"},
                                total_exposed_7: {$sum: "$7_exposed"}, total_comprehended_7: {$sum: "$7_comprehended"},
                                total_exposed_8: {$sum: "$8_exposed"}, total_comprehended_8: {$sum: "$8_comprehended"},
                                total_exposed_9: {$sum: "$9_exposed"}, total_comprehended_9: {$sum: "$9_comprehended"}}}
])


# fitness greater than a number listed descending
db.genomes.find({"fitness": {$gt: 0.2}}).sort({fitness: -1})

or

db.genomes.aggregate([
    {$match: {"fitness": {$gt: 0.2}}},
    {$sort: {fitness: -1}}
])


# listing all fitnesses above a threshold
db.genomes.aggregate([
    {$match: {"fitness": {$gt: 0.2}}},
    {$group: {_id: "$fitness"}},
    {$sort: {_id: -1}}
])


# field exist
db.getCollection('genomes').aggregate([
{$match: {fitness: {$exists: true}}},
{$project: {"genome_id": 1, "fitness": 1}}
])


﻿db.genomes.aggregate([
    {$match: {"fitness": {$gt: 0.2}}},
    {$project: {_id: "$fitness", genome_id: "$genome_id", properties: "$properties"}},
    {$sort: {_id: -1}}
])


db.genomes.aggregate([
    {$match: {}},
{$project: {_id: "$genome_id",
            fitness: "$fitness",
            location_tolerance: "$properties.location_tolerance",
            img_clr_int_tol: "$properties.image_color_intensity_tolerance",
            img_clr_int_tol: "$properties.image_color_intensity_tolerance",
            img_clr_int_tol: "$properties.image_color_intensity_tolerance",
            v11_n_cnt: "$properties.blueprint.vision_v1-1.cortical_neuron_count",
            v12_n_cnt: "$properties.blueprint.vision_v1-2.cortical_neuron_count",
            v13_n_cnt: "$properties.blueprint.vision_v1-3.cortical_neuron_count",
            v14_n_cnt: "$properties.blueprint.vision_v1-4.cortical_neuron_count",
            v15_n_cnt: "$properties.blueprint.vision_v1-5.cortical_neuron_count",
            v16_n_cnt: "$properties.blueprint.vision_v1-6.cortical_neuron_count",
            v17_n_cnt: "$properties.blueprint.vision_v1-7.cortical_neuron_count",
            v2_n_cnt: "$properties.blueprint.vision_v2.cortical_neuron_count",
            vIT_n_cnt: "$properties.blueprint.vision_IT.cortical_neuron_count"
            }},
{$sort: {fitness: -1}}
])
