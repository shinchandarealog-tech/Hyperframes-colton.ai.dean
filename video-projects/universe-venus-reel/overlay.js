/* The Universe by Venus: overlay layer (captions, text-behind-subject, liquid-glass graphics).
 * Built synchronously into one GSAP timeline in absolute video seconds.
 * Layout (font sizes, element heights) is measured once with real fonts by
 * edit-data/measure.mjs and baked into layout.js, so renders are deterministic.
 * Picks from the Universe Reel Picker: B1..B10 = C,C,C,B,B,C,C,A,C,C, sound = Clean. */
(function () {
  const FACES = [[0.446,0.502,0.486,0.534],[0.442,0.5,0.479,0.532],[0.429,0.498,0.479,0.534],[0.438,0.492,0.478,0.53],[0.429,0.488,0.476,0.526],[0.426,0.48,0.482,0.523],[0.431,0.466,0.489,0.515],[0.429,0.445,0.499,0.505],[0.435,0.415,0.514,0.489],[0.428,0.377,0.524,0.464],[0.438,0.351,0.536,0.445],[0.431,0.336,0.539,0.431],[0.425,0.321,0.542,0.421],[0.419,0.322,0.539,0.419],[0.4,0.318,0.528,0.416],[0.381,0.312,0.517,0.412],[0.367,0.305,0.5,0.399],[0.367,0.302,0.499,0.398],[0.371,0.299,0.501,0.398],[0.376,0.292,0.511,0.396],[0.383,0.292,0.517,0.397],[0.397,0.294,0.537,0.404],[0.417,0.287,0.56,0.396],[0.439,0.287,0.583,0.389],[0.457,0.286,0.593,0.391],[0.457,0.285,0.592,0.391],[0.446,0.286,0.592,0.393],[0.447,0.288,0.589,0.399],[0.442,0.291,0.585,0.402],[0.435,0.287,0.582,0.402],[0.436,0.284,0.581,0.398],[0.433,0.284,0.581,0.401],[0.44,0.281,0.596,0.402],[0.454,0.284,0.61,0.406],[0.469,0.284,0.629,0.406],[0.485,0.285,0.654,0.416],[0.517,0.275,0.679,0.417],[0.539,0.269,0.711,0.411],[0.56,0.269,0.715,0.412],[0.562,0.268,0.714,0.412],[0.558,0.267,0.71,0.423],[0.55,0.266,0.71,0.433],[0.539,0.268,0.7,0.44],[0.529,0.292,0.696,0.444],[0.524,0.266,0.689,0.437],[0.521,0.259,0.69,0.431],[0.522,0.258,0.697,0.425],[0.528,0.255,0.713,0.42],[0.543,0.255,0.729,0.413],[0.553,0.255,0.742,0.413],[0.578,0.255,0.769,0.41],[0.601,0.235,0.8,0.402],[0.628,0.227,0.822,0.381],[0.637,0.22,0.819,0.371],[0.633,0.216,0.819,0.364],[0.622,0.212,0.815,0.356],[0.614,0.212,0.799,0.354],[0.599,0.211,0.792,0.355],[0.59,0.208,0.776,0.352],[0.581,0.208,0.767,0.352],[0.575,0.211,0.761,0.355],[0.569,0.211,0.754,0.352],[0.564,0.208,0.747,0.349],[0.558,0.208,0.74,0.348],[0.553,0.207,0.729,0.344],[0.544,0.207,0.722,0.343],[0.54,0.207,0.711,0.338],[0.532,0.204,0.704,0.331],[0.525,0.204,0.696,0.327],[0.518,0.204,0.69,0.326],[0.512,0.204,0.681,0.323],[0.504,0.206,0.672,0.325],[0.497,0.207,0.664,0.328],[0.485,0.207,0.653,0.328],[0.478,0.207,0.64,0.329],[0.471,0.208,0.633,0.332],[0.467,0.211,0.624,0.332],[0.461,0.211,0.618,0.331],[0.457,0.211,0.613,0.327],[0.456,0.209,0.61,0.327],[0.454,0.207,0.608,0.327],[0.454,0.207,0.61,0.329],[0.522,0.224,0.579,0.273],[0.415,0.258,0.617,0.422],[0.411,0.256,0.628,0.423],[0.406,0.256,0.621,0.423],[0.406,0.255,0.621,0.423],[0.406,0.254,0.621,0.422],[0.407,0.255,0.621,0.419],[0.41,0.254,0.622,0.417],[0.411,0.254,0.625,0.419],[0.412,0.254,0.628,0.42],[0.407,0.251,0.621,0.419],[0.407,0.248,0.621,0.415],[0.404,0.246,0.618,0.415],[0.399,0.244,0.615,0.416],[0.403,0.243,0.617,0.417],[0.403,0.241,0.621,0.416],[0.407,0.241,0.625,0.414],[0.407,0.238,0.625,0.414],[0.396,0.235,0.614,0.411],[0.376,0.231,0.601,0.404],[0.362,0.229,0.585,0.398],[0.347,0.228,0.575,0.398],[0.344,0.23,0.567,0.398],[0.343,0.231,0.567,0.402],[0.346,0.231,0.569,0.402],[0.349,0.231,0.575,0.401],[0.353,0.231,0.576,0.402],[0.347,0.232,0.576,0.402],[0.344,0.233,0.571,0.402],[0.344,0.234,0.569,0.402],[0.344,0.234,0.569,0.403],[0.347,0.234,0.575,0.409],[0.356,0.233,0.576,0.409],[0.356,0.231,0.578,0.407],[0.356,0.23,0.578,0.402],[0.36,0.23,0.579,0.402],[0.36,0.23,0.581,0.402],[0.362,0.23,0.581,0.402],[0.362,0.229,0.576,0.399],[0.358,0.229,0.574,0.399],[0.356,0.227,0.571,0.399],[0.354,0.227,0.567,0.395],[0.353,0.227,0.567,0.395],[0.353,0.223,0.569,0.395],[0.356,0.22,0.575,0.391],[0.36,0.216,0.583,0.387],[0.364,0.216,0.585,0.385],[0.368,0.215,0.586,0.383],[0.371,0.214,0.586,0.383],[0.371,0.214,0.589,0.383],[0.371,0.214,0.589,0.382],[0.368,0.212,0.588,0.383],[0.364,0.212,0.582,0.383],[0.356,0.211,0.578,0.383],[0.351,0.209,0.569,0.381],[0.349,0.207,0.569,0.38],[0.351,0.207,0.569,0.377],[0.351,0.206,0.572,0.375],[0.354,0.203,0.574,0.373],[0.422,0.227,0.536,0.269],0,[0.388,0.493,0.446,0.543],[0.39,0.492,0.45,0.543],[0.396,0.492,0.468,0.543],[0.408,0.492,0.476,0.547],[0.418,0.49,0.496,0.549],[0.44,0.491,0.511,0.549],[0.456,0.488,0.533,0.549],[0.46,0.481,0.553,0.546],[0.472,0.481,0.568,0.549],[0.485,0.481,0.575,0.549],[0.492,0.481,0.582,0.548],[0.496,0.481,0.586,0.549],[0.5,0.481,0.596,0.548],[0.508,0.481,0.601,0.552],[0.512,0.478,0.604,0.551],[0.526,0.481,0.606,0.548],[0.514,0.473,0.61,0.548],[0.512,0.466,0.611,0.542],[0.508,0.466,0.611,0.544],[0.508,0.468,0.613,0.544],[0.508,0.466,0.614,0.542],[0.512,0.466,0.618,0.542],[0.517,0.465,0.632,0.543],[0.539,0.459,0.647,0.545],[0.553,0.459,0.674,0.545],[0.578,0.459,0.69,0.547],[0.592,0.462,0.711,0.545],[0.606,0.461,0.715,0.547],[0.594,0.461,0.714,0.551],[0.579,0.465,0.699,0.555],[0.549,0.465,0.682,0.562],[0.532,0.469,0.656,0.564],[0.519,0.466,0.643,0.563],[0.517,0.461,0.635,0.555],[0.528,0.464,0.632,0.548],[0.531,0.465,0.633,0.548],[0.517,0.458,0.635,0.548],[0.517,0.458,0.636,0.548],[0.517,0.457,0.636,0.548],[0.517,0.454,0.637,0.548],[0.517,0.453,0.639,0.548],[0.515,0.453,0.639,0.548],[0.515,0.453,0.639,0.55],[0.515,0.453,0.639,0.553],[0.515,0.453,0.643,0.553],[0.518,0.453,0.644,0.549],[0.521,0.453,0.647,0.553],[0.519,0.452,0.647,0.552],[0.518,0.452,0.646,0.554],[0.517,0.45,0.644,0.555],[0.515,0.448,0.644,0.555],[0.512,0.447,0.643,0.555],[0.506,0.449,0.642,0.553],[0.499,0.449,0.639,0.554],[0.494,0.447,0.633,0.548],[0.494,0.446,0.632,0.552],[0.493,0.448,0.635,0.553],[0.494,0.449,0.637,0.552],[0.496,0.449,0.64,0.555],[0.5,0.448,0.643,0.556],[0.501,0.446,0.644,0.557],[0.503,0.446,0.647,0.557],[0.506,0.446,0.649,0.558],[0.508,0.445,0.649,0.56],[0.508,0.445,0.653,0.561],[0.508,0.445,0.653,0.56],[0.508,0.445,0.651,0.561],[0.508,0.445,0.653,0.561],[0.508,0.442,0.653,0.562],[0.508,0.442,0.654,0.56],[0.508,0.438,0.656,0.559],[0.508,0.438,0.656,0.552],[0.504,0.438,0.656,0.555],[0.503,0.438,0.654,0.556],[0.501,0.438,0.653,0.56],[0.501,0.438,0.653,0.557],[0.501,0.437,0.654,0.558],[0.5,0.434,0.653,0.559],[0.5,0.434,0.651,0.557],[0.5,0.434,0.651,0.557],[0.403,0.395,0.487,0.459],[0.403,0.393,0.487,0.454],[0.411,0.388,0.493,0.452],[0.419,0.388,0.496,0.453],[0.415,0.391,0.507,0.456],[0.426,0.388,0.518,0.458],[0.443,0.386,0.535,0.456],[0.456,0.381,0.546,0.452],[0.454,0.38,0.553,0.45],[0.454,0.376,0.553,0.447],[0.451,0.374,0.547,0.445],[0.446,0.372,0.542,0.444],[0.431,0.37,0.535,0.445],[0.419,0.374,0.522,0.447],[0.406,0.368,0.514,0.448],[0.394,0.361,0.5,0.444],[0.385,0.362,0.492,0.442],[0.368,0.353,0.485,0.444],[0.362,0.351,0.483,0.441],[0.361,0.351,0.482,0.442],[0.36,0.348,0.486,0.444],[0.365,0.348,0.496,0.445],[0.376,0.348,0.514,0.448],[0.397,0.348,0.524,0.446],[0.4,0.345,0.539,0.452],[0.412,0.351,0.549,0.455],[0.422,0.344,0.561,0.455],[0.431,0.343,0.567,0.451],[0.432,0.341,0.569,0.452],[0.431,0.341,0.569,0.453],[0.422,0.339,0.565,0.452],[0.418,0.338,0.558,0.452],[0.41,0.221,0.592,0.424],[0.397,0.195,0.628,0.379],[0.399,0.192,0.628,0.373],[0.399,0.191,0.628,0.369],[0.399,0.191,0.628,0.369],[0.399,0.188,0.628,0.367],[0.399,0.188,0.628,0.367],[0.399,0.184,0.629,0.366],[0.403,0.184,0.633,0.366],[0.404,0.184,0.636,0.364],[0.406,0.183,0.636,0.362],[0.406,0.18,0.635,0.359],[0.406,0.18,0.635,0.359],[0.406,0.18,0.635,0.361],[0.407,0.18,0.636,0.36],[0.408,0.178,0.636,0.359],0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,[0.312,0.181,0.547,0.339],[0.328,0.182,0.562,0.34],[0.356,0.184,0.589,0.341],[0.376,0.184,0.61,0.343],[0.411,0.184,0.635,0.344],[0.418,0.188,0.653,0.347],[0.424,0.192,0.674,0.351],[0.433,0.195,0.679,0.354],[0.438,0.191,0.678,0.353],[0.435,0.191,0.675,0.352],[0.433,0.191,0.675,0.355],[0.435,0.191,0.675,0.355],[0.433,0.188,0.671,0.357],[0.431,0.188,0.672,0.356],[0.429,0.188,0.671,0.355],[0.426,0.188,0.668,0.352],[0.418,0.184,0.662,0.351],[0.414,0.184,0.656,0.351],[0.412,0.184,0.65,0.351],[0.41,0.18,0.647,0.348],[0.408,0.18,0.646,0.347],[0.408,0.18,0.649,0.347],[0.414,0.177,0.654,0.341],[0.415,0.177,0.658,0.337],[0.417,0.176,0.657,0.335],[0.414,0.172,0.654,0.332],[0.414,0.168,0.647,0.331],[0.406,0.167,0.639,0.327],[0.404,0.168,0.636,0.328],[0.406,0.168,0.635,0.329],[0.417,0.168,0.644,0.331],[0.419,0.168,0.647,0.331],[0.421,0.168,0.65,0.333],[0.422,0.167,0.65,0.333],[0.424,0.164,0.651,0.331],[0.425,0.164,0.651,0.329],[0.425,0.164,0.651,0.327],[0.426,0.164,0.651,0.329],0,[0.412,0.44,0.571,0.561],[0.414,0.438,0.574,0.563],[0.419,0.438,0.582,0.563],[0.424,0.438,0.585,0.562],[0.422,0.434,0.585,0.562],[0.422,0.434,0.582,0.559],[0.41,0.434,0.578,0.557],[0.406,0.432,0.574,0.558],[0.4,0.43,0.568,0.558],[0.399,0.43,0.567,0.555],[0.392,0.427,0.558,0.555],[0.388,0.427,0.556,0.555],[0.383,0.427,0.554,0.555],[0.381,0.427,0.553,0.555],[0.375,0.427,0.553,0.556],[0.375,0.427,0.543,0.556],0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,[0.394,0.417,0.617,0.57],[0.406,0.416,0.621,0.566],[0.418,0.415,0.621,0.563],[0.426,0.414,0.617,0.562],[0.428,0.414,0.617,0.562],[0.429,0.414,0.622,0.565],[0.431,0.414,0.625,0.565],[0.435,0.414,0.629,0.566],[0.438,0.413,0.632,0.566],[0.438,0.414,0.633,0.566],[0.435,0.413,0.632,0.566],[0.426,0.414,0.629,0.563],[0.418,0.414,0.625,0.565],[0.41,0.415,0.617,0.567],[0.407,0.415,0.614,0.57],[0.407,0.415,0.608,0.571],[0.407,0.414,0.61,0.571],[0.41,0.414,0.611,0.572],[0.408,0.41,0.613,0.571],[0.412,0.406,0.618,0.557],[0.414,0.406,0.619,0.562],[0.414,0.407,0.621,0.566],[0.414,0.407,0.622,0.564],[0.414,0.403,0.622,0.562],[0.412,0.403,0.621,0.566],[0.407,0.406,0.621,0.566],[0.406,0.403,0.618,0.566],[0.404,0.403,0.617,0.564],[0.403,0.402,0.614,0.562],[0.399,0.4,0.613,0.562],[0.396,0.4,0.61,0.566],[0.419,0.415,0.574,0.556],[0.461,0.18,0.604,0.284],[0.457,0.176,0.603,0.283],[0.45,0.173,0.597,0.281],[0.449,0.174,0.594,0.282],[0.444,0.176,0.589,0.284],[0.446,0.176,0.59,0.284],[0.449,0.18,0.596,0.288],[0.454,0.18,0.6,0.288],[0.458,0.183,0.606,0.293],[0.465,0.186,0.61,0.294],[0.468,0.188,0.614,0.294],[0.472,0.191,0.619,0.296],[0.476,0.191,0.625,0.299],[0.478,0.195,0.628,0.299],[0.481,0.195,0.629,0.3],[0.481,0.194,0.632,0.3],[0.479,0.189,0.632,0.299],[0.481,0.188,0.631,0.294],[0.483,0.188,0.636,0.294],[0.486,0.188,0.637,0.297],[0.489,0.188,0.642,0.297],[0.49,0.191,0.644,0.297],[0.489,0.191,0.649,0.298],[0.494,0.188,0.65,0.298],[0.508,0.188,0.651,0.297],[0.51,0.188,0.653,0.296],[0.512,0.189,0.656,0.298],[0.517,0.189,0.658,0.298],[0.514,0.185,0.66,0.294],[0.512,0.183,0.656,0.29],[0.51,0.184,0.657,0.289],[0.504,0.184,0.649,0.292],[0.504,0.19,0.644,0.298],[0.501,0.202,0.637,0.312],[0.507,0.227,0.633,0.345],[0.512,0.273,0.628,0.395],[0.526,0.344,0.621,0.454],[0.54,0.418,0.613,0.5],[0.543,0.466,0.608,0.528],[0.551,0.491,0.608,0.541],[0.554,0.507,0.608,0.549],[0.558,0.514,0.606,0.552],[0.56,0.514,0.607,0.553],[0.564,0.515,0.617,0.552],[0.565,0.513,0.617,0.551],[0.567,0.515,0.614,0.551],[0.568,0.513,0.621,0.552],[0.567,0.511,0.621,0.55],[0.568,0.511,0.621,0.548],[0.567,0.511,0.614,0.548],[0.562,0.509,0.617,0.549],[0.562,0.509,0.615,0.548],[0.56,0.509,0.61,0.547],[0.558,0.509,0.607,0.545],[0.556,0.507,0.607,0.546],[0.557,0.507,0.606,0.546],[0.787,0.348,0.86,0.402],[0.778,0.341,0.861,0.404],[0.776,0.341,0.858,0.405],[0.778,0.348,0.861,0.407],[0.783,0.341,0.874,0.409],[0.79,0.337,0.885,0.407],[0.801,0.337,0.893,0.406],[0.808,0.337,0.9,0.406],[0.814,0.335,0.903,0.406],[0.812,0.333,0.908,0.405],[0.818,0.333,0.911,0.408],[0.817,0.333,0.911,0.406],[0.817,0.333,0.91,0.407],[0.812,0.333,0.908,0.407],[0.811,0.333,0.906,0.407],[0.806,0.333,0.906,0.408],[0.8,0.336,0.907,0.406],[0.797,0.336,0.91,0.406],[0.797,0.334,0.914,0.406],[0.799,0.333,0.917,0.405],[0.803,0.333,0.921,0.407],[0.807,0.335,0.929,0.406],[0.81,0.336,0.932,0.408],[0.808,0.334,0.932,0.407],[0.808,0.333,0.929,0.406],[0.807,0.332,0.926,0.407],[0.807,0.332,0.926,0.406],[0.807,0.332,0.928,0.406],[0.807,0.332,0.926,0.406],[0.807,0.332,0.926,0.405],[0.807,0.332,0.926,0.405],[0.811,0.332,0.925,0.404],[0.819,0.33,0.921,0.403],[0.818,0.33,0.917,0.404],[0.817,0.33,0.912,0.399],[0.808,0.329,0.906,0.402],[0.803,0.333,0.899,0.401],[0.789,0.33,0.892,0.403],[0.783,0.332,0.882,0.402],[0.779,0.331,0.878,0.401],[0.778,0.331,0.874,0.401],[0.775,0.33,0.874,0.402],[0.775,0.329,0.874,0.402],[0.775,0.329,0.874,0.401],[0.776,0.329,0.874,0.401],0,0,0,0,0,0,[0.224,0.467,0.357,0.566],[0.169,0.326,0.379,0.584],0,0,[0.15,0.395,0.414,0.595],[0.34,0.453,0.4,0.52],0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]; // head box per 0.1 s, normalized [x0,y0,x1,y1] or 0 (from edit-data/faces.json)
  const PICK = { b1: "C", b2: "C", b3: "C", b4: "B", b5: "B", b6: "C", b7: "C", b8: "A", b9: "C", b10: "C" };
  const BEATS = [
    { id: "b1", s: 0, e: 8.0, y: .58,
      ph: [{ t: 0.1, et: 1.0, end: 1.85, k: "Ahmedabad mein", e: "ADDRESS" }, { t: 1.85, et: 2.9, end: 3.96, k: "sirf yeh nahi ki", e: "AAP KAHAN REHTE HO", sweep: 1 },
           { t: 3.96, et: 5.45, end: 6.1, k: "balki is baat se bhi", e: "JUDA HAI" }, { t: 6.1, et: 7.4, end: 8.0, k: "ki aap kin cheezon ke", e: "KAREEB HO" }],
      C: { type: "place", t: 1.0, end: 3.9, title: "Ahmedabad", sub: "Gujarat, India" } },
    { id: "b2", s: 8.0, e: 14.0, y: .62,
      ph: [{ t: 8.02, et: 9.1, end: 9.68, k: "aapke subah ke", e: "DARSHAN" }, { t: 9.68, et: 10.8, end: 11.67, k: "aapka parivaar,", e: "AAPKA SAMAAJ" },
           { t: 11.67, et: 12.48, end: 14.0, k: "sab kuch", e: "AAPKI PAHUNCH MEIN", sweep: 1 }],
      C: { type: "check", t: 9.0, end: 14.0, title: "Aapki pahunch mein", items: [["Subah ke darshan", 9.1], ["Parivaar", 10.3], ["Samaaj", 11.3]] } },
    { id: "b3", s: 14.0, e: 22.0, y: .40,
      ph: [{ t: 14.0, et: 15.5, end: 16.05, k: "kai parivaaron ke liye", e: "GHAR KE PAAS" }, { t: 16.05, et: 16.1, end: 17.1, k: "", e: "DERASAR HONA" },
           { t: 17.13, et: 18.0, end: 19.0, k: "suvidha se", e: "KAHIN ZYADA HAI" }, { t: 19.02, et: 20.7, end: 22.0, k: "aapki roz-marra ki zindagi ka", e: "HISSA BAN JAATA HAI" }],
      C: { type: "pill", t: 16.1, end: 19.0, text: "Derasar, ghar ke paas" } },
    { id: "b4", s: 22.0, e: 25.0, y: .55,
      ph: [{ t: 22.0, et: 23.2, end: 25.0, k: "woh pata jo", e: "GHAR JAISA", tail: { t: 24.17, text: "mehsoos karaata hai" } }] },
    { id: "b5", s: 25.0, e: 29.27, y: .55,
      ph: [{ t: 25.0, et: 26.92, end: 27.5, k: "kyunki jab kisi jagah par", e: "PEHLE SE HI" }, { t: 27.5, et: 28.13, end: 29.27, k: "ghar jaisa", e: "MEHSOOS HONE LAGTA HAI", sweep: 1 }] },
    { id: "b6", s: 29.27, e: 32.5, y: .62,
      ph: [{ t: 29.9, et: 30.0, end: 32.5, k: "yeh sab", e: "AAPKE LIYE" }],
      C: { type: "note", t: 30.0, end: 32.5, title: "The Universe by Venus", body: "Aapka ghar, aapke liye." } },
    { id: "b7", s: 32.5, e: 40.6, y: .55,
      ph: [{ t: 32.55, et: 33.84, end: 34.7, k: "aur jab aapka ghar", e: "AHMEDABAD KI" }, { t: 34.7, et: 34.99, end: 36.2, k: "sabse", e: "PRIME LOCATION", sweep: 1 },
           { t: 36.2, et: 36.57, end: 37.6, k: "mein se ek,", e: "NEHRU NAGAR" }, { t: 37.6, et: 38.65, end: 40.6, k: "to suvidha", e: "APNE AAP AA JAATI HAI" }],
      C: { type: "place", t: 36.5, end: 40.6, title: "Nehru Nagar", sub: "Ahmedabad · 23.02° N, 72.55° E" } },
    { id: "b8", s: 40.6, e: 46.3, y: .30,
      ph: [{ t: 41.0, et: 42.97, end: 43.9, k: "aur theek in sab ke", e: "BEECH MEIN" }, { t: 43.9, et: 44.6, end: 46.3, k: "aata hai", e: "VENUS THE UNIVERSE" }] },
    { id: "b9", s: 46.3, e: 50.77, y: .40,
      ph: [{ t: 46.3, et: 46.45, end: 49.4, k: "", e: "THE UNIVERSE" }, { t: 49.4, et: 49.5, end: 50.77, k: "by", e: "VENUS" }],
      C: { type: "pill", t: 46.9, end: 50.77, text: "Nehru Nagar, Ahmedabad" } },
    { id: "b10", s: 50.77, e: 56.2, y: .68, avoid: [{ y0: .28, y1: .695 }], bot: .9,
      ph: [{ t: 52.4, et: 53.0, end: 56.2, k: "come,", e: "EXPERIENCE THE ADDRESS", sweep: 1 }],
      C: { type: "pill", t: 53.8, end: 56.2, text: "Nehru Nagar · Ahmedabad" } }
  ];
  const F = 1 / 30, TOP_SAFE = .13, BOT_SAFE = .80; let BOT = BOT_SAFE;
  const snap = (t) => Math.round(t * 30) / 30;

  /* ---- layout: record (measure page) or replay (render) ---- */
  const LAYOUT = window.__LAYOUT; const REC = []; let li = 0;
  function measure(fn) { if (LAYOUT) return LAYOUT[li++]; const v = fn(); REC.push(v); li++; return v; }
  function fit(node, base, target, min, max) {
    const fs = measure(() => { node.style.fontSize = base + "px"; const w = node.offsetWidth || 1; return Math.round(Math.max(min, Math.min(max, base * target / w)) * 10) / 10; });
    node.style.fontSize = fs + "px";
  }
  const hOf = (node) => measure(() => Math.round(node.offsetHeight * 10) / 10) / 1920;
  const wOf = (node) => measure(() => node.offsetWidth);

  function el(tag, cls, parent, html) { const n = document.createElement(tag); if (cls) n.className = cls; if (html != null) n.innerHTML = html; if (parent) parent.appendChild(n); return n; }
  function esc(s) { return s.replace(/&/g, "&amp;").replace(/</g, "&lt;"); }
  function words(node, text) { return text.split(/\s+/).filter(Boolean).map((w) => el("span", null, node, esc(w))); }
  function faceIn(t0, t1) {
    let b = null;
    for (let i = Math.max(0, Math.floor(t0 * 10)); i <= Math.min(FACES.length - 1, Math.floor((t1 - 0.1) * 10)); i++) {
      const f = FACES[i]; if (!f) continue;
      b = b ? [Math.min(b[0], f[0]), Math.min(b[1], f[1]), Math.max(b[2], f[2]), Math.max(b[3], f[3])] : f.slice();
    }
    return b ? { y0: b[1] - .025, y1: b[3] + .03 } : null;
  }
  function placeSlot(h, obs, prefer) {
    const half = h / 2, lo = TOP_SAFE + half, hi = BOT - half;
    const cands = [prefer]; obs.forEach((o) => { cands.push(o.y1 + .015 + half, o.y0 - .015 - half); });
    const ok = (c) => c >= lo && c <= hi && obs.every((o) => c + half <= o.y0 || c - half >= o.y1);
    const good = cands.filter(ok).sort((a, b) => Math.abs(a - prefer) - Math.abs(b - prefer));
    if (good.length) return good[0];
    return Math.min(hi, Math.max(lo, obs.length ? Math.max(...obs.map((o) => o.y1)) + .015 + half : prefer));
  }
  function caption(layer, p) {
    const g = el("div", "grp", layer); let kw = [], ew = [], eNode = null, tw = [];
    if (p.k) { const k = el("div", "k", g); kw = words(k, p.k); }
    if (p.e) { eNode = el("div", "e", g); ew = words(eNode, p.e); fit(eNode, 96, 800, 58, 150); }
    if (p.tail) { const t = el("div", "k tail", g); tw = words(t, p.tail.text); }
    return { g, kw, ew, eNode, tw, h: hOf(g) };
  }
  function animKicker(tl, kw, t0, span) {
    const gap = kw.length > 1 ? Math.min(.22, span / kw.length) : 0;
    kw.forEach((w, i) => tl.fromTo(w, { opacity: 0, y: -18, filter: "blur(4px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 3 * F, ease: "power2.out" }, snap(t0 + i * gap)));
  }
  function animEmph(tl, ew, t0) {
    ew.forEach((w, i) => tl.fromTo(w, { opacity: 0, x: -90, filter: "blur(14px)" }, { opacity: 1, x: 0, filter: "blur(0px)", duration: 4 * F, ease: "expo.out" }, snap(t0 + i * 2 * F)));
  }

  /* ---- A: kinetic stack, face-safe ---- */
  function captionsFront(L, b, tl, extraObs) {
    b.ph.forEach((p) => {
      const c = caption(L.front, p); const all = [...c.kw, ...c.ew, ...c.tw];
      const kn = [...c.g.querySelectorAll('.k')];
      const obs = [...(b.avoid || [])]; const f = faceIn(p.t, p.end); if (f) obs.push(f);
      (extraObs || []).forEach((o) => { if (o.t0 < p.end && o.t1 > p.t) obs.push(o); });
      c.g.style.top = (placeSlot(c.h, obs, b.y) * 1920) + "px";
      tl.set(all, { opacity: 0 }, 0);
      const t0 = p.t - b.s, te = p.et - b.s, end = snap(p.end - b.s);
      animKicker(tl, c.kw, t0, Math.max(.1, te - t0 - .05)); animEmph(tl, c.ew, te);
      if (p.tail) animKicker(tl, c.tw, p.tail.t - b.s, .3);
      if (p.sweep && c.eNode) {
        const s = el("div", "sweep", c.eNode); tl.set(s, { scaleX: 0, opacity: 0 }, 0);
        tl.set(s, { opacity: 1 }, snap(te + .35)).fromTo(s, { scaleX: 0 }, { scaleX: 1, duration: .3333, ease: "power2.inOut" }, snap(te + .35)).to(s, { opacity: 0, duration: .2 }, snap(te + .7333));
      }
      tl.set(all, { opacity: 0 }, end);
      if (kn.length) { tl.set(kn, { opacity: 0 }, 0); tl.set(kn[0], { opacity: 1 }, snap(t0)); if (kn[1]) tl.set(kn[1], { opacity: 1 }, snap(p.tail ? p.tail.t - b.s : t0)); tl.set(kn, { opacity: 0 }, end); }
    });
  }
  function buildA(L, b) { BOT = b.bot || BOT_SAFE; const tl = gsap.timeline(); captionsFront(L, b, tl); tl.to({}, { duration: b.e - b.s }, 0); return tl; }

  /* ---- B: big text behind the subject (person cutout video sits between layers) ---- */
  function splitLines(t) {
    const w = t.split(" "); if (t.length <= 11 || w.length < 2) return [t];
    let best = 1, bd = 1e9; for (let i = 1; i < w.length; i++) { const d = Math.abs(w.slice(0, i).join(" ").length - w.slice(i).join(" ").length); if (d < bd) { bd = d; best = i; } }
    return [w.slice(0, best).join(" "), w.slice(best).join(" ")];
  }
  function buildB(L, b) {
    BOT = b.bot || BOT_SAFE; const tl = gsap.timeline();
    b.ph.forEach((p) => {
      const t0 = p.t - b.s, te = p.et - b.s, end = snap(p.end - b.s);
      const big = el("div", "big", L.back); const lines = splitLines(p.e).map((s) => { const d = el("div", "ln", big, esc(s)); fit(d, 200, 920, 56, 330); return d; });
      const bh = hOf(big); const f = faceIn(p.t, p.end);
      const yc = f ? Math.max(TOP_SAFE + bh / 2, Math.min(.62, f.y0 + .02 + bh * .18)) : placeSlot(bh, b.avoid || [], b.y);
      big.style.top = (yc * 1920) + "px";
      tl.set(lines, { opacity: 0 }, 0);
      lines.forEach((ln, i) => tl.fromTo(ln, { opacity: 0, yPercent: 40, scale: 1.12, filter: "blur(18px)" }, { opacity: 1, yPercent: 0, scale: 1, filter: "blur(0px)", duration: .3333, ease: "power3.out" }, snap(te + i * .08)));
      tl.to(lines, { scale: 1.04, duration: snap(Math.max(.2, end - te - .1)), ease: "none" }, snap(te + .3333));
      tl.set(lines, { opacity: 0 }, end);
      if (p.k || p.tail) {
        const g = el("div", "grp", L.front); let kw = []; if (p.k) { const k = el("div", "k", g); kw = words(k, p.k); }
        let tw = []; if (p.tail) { const t = el("div", "k", g); t.style.fontSize = "46px"; tw = words(t, p.tail.text); }
        const kh = hOf(g); const obs = [...(b.avoid || [])]; if (f) obs.push(f); if (!f) obs.push({ y0: yc - bh / 2, y1: yc + bh / 2 });
        g.style.top = (placeSlot(kh, obs, yc - bh / 2 - kh / 2 - .01) * 1920) + "px";
        tl.set([...kw, ...tw], { opacity: 0 }, 0); animKicker(tl, kw, t0, Math.max(.1, te - t0)); if (p.tail) animKicker(tl, tw, p.tail.t - b.s, .3);
        tl.set([...kw, ...tw], { opacity: 0 }, end);
        const kn = [...g.querySelectorAll('.k')]; tl.set(kn, { opacity: 0 }, 0); tl.set(kn[0], { opacity: 1 }, snap(t0)); if (kn[1]) tl.set(kn[1], { opacity: 1 }, snap(p.tail.t - b.s)); tl.set(kn, { opacity: 0 }, end);
      }
    });
    tl.to({}, { duration: b.e - b.s }, 0); return tl;
  }

  /* ---- C: liquid-glass graphics + face-safe captions ---- */
  const ICON_PIN = '<svg viewBox="0 0 24 24"><path d="M12 2C8.1 2 5 5.1 5 9c0 5.2 7 13 7 13s7-7.8 7-13c0-3.9-3.1-7-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z" fill="#fff"/></svg>';
  const ICON_CHECK = '<svg viewBox="0 0 30 30"><path d="M6 16l6 6 12-14" fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  const ICON_U = '<svg viewBox="0 0 24 24" width="34" height="34"><path d="M6 3v10a6 6 0 0 0 12 0V3" fill="none" stroke="#D9B46A" stroke-width="2"/><path d="M9 3v10a3 3 0 0 0 6 0V3" fill="none" stroke="#D9B46A" stroke-width="1.5"/></svg>';
  function glass(parent, cls, width) { const g = el("div", "glass " + (cls || ""), parent); if (width) { g.style.width = width + "px"; g.style.left = ((1080 - width) / 2) + "px"; } el("div", "sheen", g); return { g, inn: el("div", "in", g) }; }
  function sheen(tl, g, t) { tl.fromTo(g.querySelector(".sheen"), { x: 0 }, { x: 1700, duration: .9, ease: "power2.inOut" }, snap(t)); }
  function popIn(tl, node, t) { tl.fromTo(node, { opacity: 0, y: 40, scale: .9, filter: "blur(10px)" }, { opacity: 1, y: 0, scale: 1, filter: "blur(0px)", duration: .4333, ease: "back.out(1.6)" }, snap(t)); }
  function buildC(L, b) {
    BOT = b.bot || BOT_SAFE; const tl = gsap.timeline(); const C = b.C; const t0 = C.t - b.s, end = snap(C.end - b.s);
    let node, prefer = .62;
    if (C.type === "place") {
      const { g, inn } = glass(L.front, "", 780); node = g;
      const r = el("div", "g-row", inn); el("div", "g-ico", r, ICON_PIN); const tx = el("div", null, r); el("div", "g-t1", tx, esc(C.title)); el("div", "g-t2", tx, esc(C.sub));
      popIn(tl, g, t0); tl.fromTo(r.querySelector(".g-ico"), { y: -60, opacity: 0 }, { y: 0, opacity: 1, duration: .5, ease: "bounce.out" }, snap(t0 + .1)); sheen(tl, g, t0 + .35);
    } else if (C.type === "check") {
      const { g, inn } = glass(L.front, "", 700); node = g;
      el("div", "g-lbl", inn, esc(C.title)); popIn(tl, g, t0);
      C.items.forEach(([txt, t]) => {
        const r = el("div", "g-ck", inn); const bx = el("div", "bx", r); const f = el("div", "fill", bx); bx.insertAdjacentHTML("beforeend", ICON_CHECK); el("span", null, r, esc(txt));
        const path = bx.querySelector("path"); const lt = snap(t - b.s);
        tl.set(r, { opacity: .45 }, 0).set(f, { scale: 0 }, 0).set(path, { strokeDasharray: 30, strokeDashoffset: 30 }, 0)
          .to(r, { opacity: 1, duration: .1333 }, lt).to(f, { scale: 1, duration: .1667, ease: "back.out(2)" }, lt).to(path, { strokeDashoffset: 0, duration: .2 }, snap(lt + .0667));
      });
      sheen(tl, g, t0 + .3);
    } else if (C.type === "pill") {
      const { g, inn } = glass(L.front, "g-pill", null); node = g; el("span", "dot", inn); el("span", null, inn, esc(C.text));
      g.style.left = "50%"; popIn(tl, g, t0); tl.set(g, { xPercent: -50 }, 0); sheen(tl, g, t0 + .25);
      tl.fromTo(inn.querySelector(".dot"), { scale: .6 }, { scale: 1.15, duration: .5, repeat: 5, yoyo: true, ease: "sine.inOut" }, snap(t0 + .3));
    } else if (C.type === "note") {
      const { g, inn } = glass(L.front, "g-note", 900); node = g; prefer = .2;
      el("div", "app", inn, '<span class="mini">' + ICON_U + '</span><span>Universe</span><span class="when">now</span>'); el("div", "tt", inn, esc(C.title)); el("div", "bd", inn, esc(C.body));
      tl.fromTo(g, { opacity: 0, yPercent: -120, scale: .94 }, { opacity: 1, yPercent: 0, scale: 1, duration: .5, ease: "back.out(1.3)" }, snap(t0)); sheen(tl, g, t0 + .4);
    }
    const h = hOf(node); const f = faceIn(C.t, C.end); const top = placeSlot(h, [...(b.avoid || []), ...(f ? [f] : [])], prefer) - h / 2;
    node.style.top = (top * 1920) + "px"; tl.set(node, { opacity: 0 }, 0); tl.set(node, { opacity: 0 }, end);
    captionsFront(L, b, tl, [{ y0: top - .01, y1: top + h + .01, t0: C.t, t1: C.end }]);
    tl.to({}, { duration: b.e - b.s }, 0); return tl;
  }
  const BUILD = { A: buildA, B: buildB, C: buildC };

  /* ---- assemble: one master timeline in absolute seconds ---- */
  window.buildUniverseOverlay = function (back, front, total) {
    const master = gsap.timeline({ paused: true }); /* children below are unpaused: a paused child never moves with its parent */ const events = [];
    BEATS.forEach((b) => {
      const v = PICK[b.id]; const bL = el("div", "beat-layer", back), fL = el("div", "beat-layer", front);
      bL.id = b.id + "-back"; fL.id = b.id + "-front";
      const tl = BUILD[v]({ back: bL, front: fL }, b);
      master.set([bL, fL], { opacity: 1 }, b.s).set([bL, fL], { opacity: 0 }, b.e);
      master.add(tl, b.s);
      b.ph.forEach((p) => { if (p.e) events.push({ t: p.et, kind: "emph" }); });
      if (v === "C") events.push({ t: b.C.t, kind: b.C.type === "note" ? "note" : "ui" });
    });
    master.to({}, { duration: total }, 0);
    window.__REC = REC; window.__SFX_EVENTS = events;
    return master;
  };
})();
