{
	"patcher" : 	{
		"fileversion" : 1,
		"appversion" : 		{
			"major" : 8,
			"minor" : 1,
			"revision" : 3,
			"architecture" : "x64",
			"modernui" : 1
		}
,
		"classnamespace" : "box",
		"rect" : [ 59.0, 104.0, 1121.0, 912.0 ],
		"bglocked" : 0,
		"openinpresentation" : 0,
		"default_fontsize" : 12.0,
		"default_fontface" : 0,
		"default_fontname" : "Arial",
		"gridonopen" : 1,
		"gridsize" : [ 15.0, 15.0 ],
		"gridsnaponopen" : 1,
		"objectsnaponopen" : 1,
		"statusbarvisible" : 2,
		"toolbarvisible" : 1,
		"lefttoolbarpinned" : 0,
		"toptoolbarpinned" : 0,
		"righttoolbarpinned" : 0,
		"bottomtoolbarpinned" : 0,
		"toolbars_unpinned_last_save" : 0,
		"tallnewobj" : 0,
		"boxanimatetime" : 200,
		"enablehscroll" : 1,
		"enablevscroll" : 1,
		"devicewidth" : 0.0,
		"description" : "",
		"digest" : "",
		"tags" : "",
		"style" : "",
		"subpatcher_template" : "",
		"boxes" : [ 			{
				"box" : 				{
					"id" : "obj-68",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ -71.0, 565.0, 52.0, 22.0 ],
					"text" : "expr $f1"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-62",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ -60.0, 223.0, 91.0, 22.0 ],
					"presentation_linecount" : 2,
					"text" : "custom -2 0 2 3"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-61",
					"linecount" : 3,
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 9.0, -102.0, 410.0, 47.0 ],
					"text" : "must pull MLE repo from github\n\ngithub.com/collaborative-music-lab/MLE"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-58",
					"maxclass" : "preset",
					"numinlets" : 1,
					"numoutlets" : 4,
					"outlettype" : [ "preset", "int", "preset", "int" ],
					"patching_rect" : [ -219.0, -15.0, 100.0, 40.0 ],
					"preset_data" : [ 						{
							"number" : 1,
							"data" : [ 5, "obj-45", "live.grid", "mode", 0, 5, "obj-45", "live.grid", "matrixmode", 0, 5, "obj-45", "live.grid", "columns", 16, 5, "obj-45", "live.grid", "rows", 16, 21, "obj-45", "live.grid", "constraint", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 21, "obj-45", "live.grid", "constraint", 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 21, "obj-45", "live.grid", "constraint", 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 21, "obj-45", "live.grid", "constraint", 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 21, "obj-45", "live.grid", "constraint", 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 21, "obj-45", "live.grid", "constraint", 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 21, "obj-45", "live.grid", "constraint", 7, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 21, "obj-45", "live.grid", "constraint", 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 21, "obj-45", "live.grid", "constraint", 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 21, "obj-45", "live.grid", "constraint", 10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 21, "obj-45", "live.grid", "constraint", 11, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 21, "obj-45", "live.grid", "constraint", 12, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 21, "obj-45", "live.grid", "constraint", 13, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 21, "obj-45", "live.grid", "constraint", 14, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 21, "obj-45", "live.grid", "constraint", 15, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 21, "obj-45", "live.grid", "constraint", 16, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 20, "obj-45", "live.grid", "steps", 3, 3, 4, 4, 5, 6, 6, 7, 8, 8, 4, 4, 3, 3, 3, 16, 20, "obj-45", "live.grid", "directions", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ]
						}
, 						{
							"number" : 2,
							"data" : [ 5, "obj-45", "live.grid", "mode", 0, 5, "obj-45", "live.grid", "matrixmode", 0, 5, "obj-45", "live.grid", "columns", 16, 5, "obj-45", "live.grid", "rows", 16, 21, "obj-45", "live.grid", "constraint", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 21, "obj-45", "live.grid", "constraint", 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 21, "obj-45", "live.grid", "constraint", 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 21, "obj-45", "live.grid", "constraint", 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 21, "obj-45", "live.grid", "constraint", 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 21, "obj-45", "live.grid", "constraint", 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 21, "obj-45", "live.grid", "constraint", 7, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 21, "obj-45", "live.grid", "constraint", 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 21, "obj-45", "live.grid", "constraint", 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 21, "obj-45", "live.grid", "constraint", 10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 21, "obj-45", "live.grid", "constraint", 11, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 21, "obj-45", "live.grid", "constraint", 12, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 21, "obj-45", "live.grid", "constraint", 13, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 21, "obj-45", "live.grid", "constraint", 14, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 21, "obj-45", "live.grid", "constraint", 15, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 21, "obj-45", "live.grid", "constraint", 16, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 20, "obj-45", "live.grid", "steps", 3, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 1, 1, 1, 20, "obj-45", "live.grid", "directions", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ]
						}
 ]
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-57",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 356.0, 235.0, 29.5, 22.0 ],
					"text" : "2"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-55",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 318.0, 235.0, 29.5, 22.0 ],
					"text" : "1"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-53",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 256.0, 236.0, 45.0, 22.0 ],
					"text" : "store 1"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-51",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 592.0, 259.0, 150.0, 20.0 ],
					"text" : "shiftl click to store"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-49",
					"maxclass" : "preset",
					"numinlets" : 1,
					"numoutlets" : 4,
					"outlettype" : [ "preset", "int", "preset", "int" ],
					"patching_rect" : [ 490.0, 245.0, 100.0, 40.0 ],
					"pattrstorage" : "moogPM"
				}

			}
, 			{
				"box" : 				{
					"active" : 					{
						"MLE.analogueDrums" : 0,
						"MLE.analogueDrums::kickTuning" : 0,
						"MLE.analogueDrums::kickSweep" : 0,
						"MLE.analogueDrums::kickDecay" : 0,
						"MLE.analogueDrums::kickAttack" : 0,
						"MLE.analogueDrums::kickLevel" : 0,
						"MLE.analogueDrums::snareTuning" : 0,
						"MLE.analogueDrums::snareDecay" : 0,
						"MLE.analogueDrums::snareSnap" : 0,
						"MLE.analogueDrums::snareHicut" : 0,
						"MLE.analogueDrums::snareLevel" : 0,
						"MLE.analogueDrums::hihatTone" : 0,
						"MLE.analogueDrums::hihatCloseDecay" : 0,
						"MLE.analogueDrums::hihatOpDecay" : 0,
						"MLE.analogueDrums::hihatLevel" : 0,
						"MLE.analogueDrums::tomLow" : 0,
						"MLE.analogueDrums::tomMid" : 0,
						"MLE.analogueDrums::tomHi" : 0,
						"MLE.analogueDrums::tomDecay" : 0,
						"MLE.analogueDrums::tomLevel" : 0,
						"MLE.analogueDrums::aDrumLevel" : 0,
						"MLE.analogueDrums::u729001988" : 0,
						"MLE.analogueDrums::accent" : 0,
						"MLE.analogueDrums::choke" : 0,
						"MLE.analogueDrums::live.button" : 0,
						"MLE.analogueDrums::live.button[1]" : 0,
						"MLE.analogueDrums::live.button[2]" : 0,
						"MLE.analogueDrums::live.button[3]" : 0,
						"MLE.analogueDrums::live.button[4]" : 0,
						"MLE.analogueDrums::live.button[5]" : 0,
						"MLE.analogueDrums::live.button[6]" : 0,
						"MLE.analogueDrums::live.button[7]" : 0,
						"MLE.analogueDrums::live.button[8]" : 0
					}
,
					"id" : "obj-46",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 256.0, 263.0, 186.0, 22.0 ],
					"saved_object_attributes" : 					{
						"client_rect" : [ 4, 79, 604, 1016 ],
						"parameter_enable" : 0,
						"parameter_mappable" : 0,
						"storage_rect" : [ 583, 69, 1034, 197 ]
					}
,
					"text" : "pattrstorage moogPM @greedy 1",
					"varname" : "moogPM"
				}

			}
, 			{
				"box" : 				{
					"direction" : 0,
					"id" : "obj-45",
					"maxclass" : "live.grid",
					"numinlets" : 2,
					"numoutlets" : 6,
					"outlettype" : [ "", "", "", "", "", "" ],
					"parameter_enable" : 1,
					"patching_rect" : [ -238.0, 27.0, 300.0, 150.0 ],
					"saved_attribute_attributes" : 					{
						"valueof" : 						{
							"parameter_invisible" : 1,
							"parameter_shortname" : "live.grid",
							"parameter_type" : 3,
							"parameter_longname" : "live.grid"
						}

					}
,
					"varname" : "live.grid"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-44",
					"maxclass" : "newobj",
					"numinlets" : 5,
					"numoutlets" : 4,
					"outlettype" : [ "int", "", "", "int" ],
					"patching_rect" : [ -238.0, -46.0, 69.0, 22.0 ],
					"text" : "counter 1 8"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-39",
					"maxclass" : "number",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "bang" ],
					"parameter_enable" : 0,
					"patching_rect" : [ -85.0, 271.0, 50.0, 22.0 ]
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-37",
					"maxclass" : "toggle",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "int" ],
					"parameter_enable" : 0,
					"patching_rect" : [ -240.0, -142.0, 24.0, 24.0 ]
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-35",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "bang" ],
					"patching_rect" : [ -240.0, -95.0, 63.0, 22.0 ],
					"text" : "metro 120"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-34",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ -155.0, 377.0, 34.0, 22.0 ],
					"text" : "pack"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-33",
					"maxclass" : "newobj",
					"numinlets" : 3,
					"numoutlets" : 2,
					"outlettype" : [ "float", "float" ],
					"patching_rect" : [ -160.0, 339.0, 108.0, 22.0 ],
					"text" : "makenote 100 100"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-31",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ -164.0, 223.0, 87.0, 22.0 ],
					"text" : "custom 0 2 5 7"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-29",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "float" ],
					"patching_rect" : [ -160.0, 302.0, 65.0, 22.0 ],
					"text" : "MLE.scale"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-28",
					"maxclass" : "nodes",
					"nodesnames" : [ "1" ],
					"nsize" : [ 0.2 ],
					"numinlets" : 1,
					"numoutlets" : 3,
					"outlettype" : [ "", "", "" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 976.0, 50.0, 100.0, 100.0 ],
					"xplace" : [ 0.083333333333333 ],
					"yplace" : [ 0.083333333333333 ]
				}

			}
, 			{
				"box" : 				{
					"active" : 					{
						"PM1" : 0,
						"MLE.moog" : 0,
						"MLE.moog::u046004795" : 0,
						"MLE.moog::AM2-1" : 0,
						"MLE.moog::FM3-1" : 0,
						"MLE.moog::VCAgate" : 0,
						"MLE.moog::amoLFO" : 0,
						"MLE.moog::ampADSR" : 0,
						"MLE.moog::filterADSR" : 0,
						"MLE.moog::filterADSRlevel" : 0,
						"MLE.moog::filterFreq" : 0,
						"MLE.moog::filterKey" : 0,
						"MLE.moog::filterLFO" : 0,
						"MLE.moog::filterRes" : 0,
						"MLE.moog::glide" : 0,
						"MLE.moog::lfoFreq" : 0,
						"MLE.moog::lfoShape" : 0,
						"MLE.moog::masterVolume" : 0,
						"MLE.moog::mono" : 0,
						"MLE.moog::noiseColor" : 0,
						"MLE.moog::noiseGain" : 0,
						"MLE.moog::osc1_octave" : 0,
						"MLE.moog::osc1_waveform" : 0,
						"MLE.moog::osc1duty" : 0,
						"MLE.moog::osc1gain" : 0,
						"MLE.moog::osc2_waveform" : 0,
						"MLE.moog::osc2detune" : 0,
						"MLE.moog::osc2duty" : 0,
						"MLE.moog::osc2gain" : 0,
						"MLE.moog::osc2octave" : 0,
						"MLE.moog::osc3-waveform" : 0,
						"MLE.moog::osc3detune" : 0,
						"MLE.moog::osc3duty" : 0,
						"MLE.moog::osc3gain" : 0,
						"MLE.moog::osc3octave" : 0,
						"MLE.moog::pitchLFO" : 0,
						"MLE.moog::pwmLFO" : 0,
						"MLE.moog::slop" : 0
					}
,
					"id" : "obj-27",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 1077.0, 161.0, 163.0, 22.0 ],
					"saved_object_attributes" : 					{
						"client_rect" : [ 4, 79, 604, 1016 ],
						"parameter_enable" : 0,
						"parameter_mappable" : 0,
						"storage_rect" : [ 583, 69, 1034, 197 ]
					}
,
					"text" : "pattrstorage PM2 @greedy 1",
					"varname" : "PM2"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-26",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 1184.0, 49.0, 45.0, 22.0 ],
					"text" : "store 1"
				}

			}
, 			{
				"box" : 				{
					"format" : 6,
					"id" : "obj-23",
					"maxclass" : "flonum",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "bang" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 1274.0, 60.0, 50.0, 22.0 ]
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-21",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 1274.0, 94.0, 188.0, 22.0 ],
					"text" : "pattrforward MLE.moog::filterFreq"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-20",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 1084.0, 50.0, 77.0, 22.0 ],
					"text" : "clientwindow"
				}

			}
, 			{
				"box" : 				{
					"active" : 					{
						"MLE.analogueDrums" : 0,
						"MLE.analogueDrums::u808001799" : 0,
						"MLE.analogueDrums::kickTuning" : 0,
						"MLE.analogueDrums::kickSweep" : 0,
						"MLE.analogueDrums::kickDecay" : 0,
						"MLE.analogueDrums::kickAttack" : 0,
						"MLE.analogueDrums::kickLevel" : 0,
						"MLE.analogueDrums::snareTuning" : 0,
						"MLE.analogueDrums::snareDecay" : 0,
						"MLE.analogueDrums::snareSnap" : 0,
						"MLE.analogueDrums::snareHicut" : 0,
						"MLE.analogueDrums::snareLevel" : 0,
						"MLE.analogueDrums::hihatTone" : 0,
						"MLE.analogueDrums::hihatCloseDecay" : 0,
						"MLE.analogueDrums::hihatOpDecay" : 0,
						"MLE.analogueDrums::hihatLevel" : 0,
						"MLE.analogueDrums::tomLow" : 0,
						"MLE.analogueDrums::tomMid" : 0,
						"MLE.analogueDrums::tomHi" : 0,
						"MLE.analogueDrums::tomDecay" : 0,
						"MLE.analogueDrums::tomLevel" : 0,
						"MLE.analogueDrums::aDrumLevel" : 0,
						"MLE.analogueDrums::u729001988" : 0,
						"MLE.analogueDrums::accent" : 0,
						"MLE.analogueDrums::choke" : 0,
						"MLE.analogueDrums::live.button" : 0,
						"MLE.analogueDrums::live.button[1]" : 0,
						"MLE.analogueDrums::live.button[2]" : 0,
						"MLE.analogueDrums::live.button[3]" : 0,
						"MLE.analogueDrums::live.button[4]" : 0,
						"MLE.analogueDrums::live.button[5]" : 0,
						"MLE.analogueDrums::live.button[6]" : 0,
						"MLE.analogueDrums::live.button[7]" : 0,
						"MLE.analogueDrums::live.button[8]" : 0,
						"MLE.FMsynth" : 0,
						"MLE.FMsynth::u593015438" : 0,
						"MLE.FMsynth::carrier2ratio" : 0,
						"MLE.FMsynth::env1a" : 0,
						"MLE.FMsynth::env2a" : 0,
						"MLE.FMsynth::env2d" : 0,
						"MLE.FMsynth::env2d[1]" : 0,
						"MLE.FMsynth::env2r" : 0,
						"MLE.FMsynth::env2r[1]" : 0,
						"MLE.FMsynth::env2response" : 0,
						"MLE.FMsynth::env2s" : 0,
						"MLE.FMsynth::env2s[1]" : 0,
						"MLE.FMsynth::mod1depth" : 0,
						"MLE.FMsynth::mod1env" : 0,
						"MLE.FMsynth::mod1harm" : 0,
						"MLE.FMsynth::mod2depth" : 0,
						"MLE.FMsynth::mod2env" : 0,
						"MLE.FMsynth::mod2harm" : 0,
						"MLE.FMsynth::osc2e" : 0,
						"PM2" : 0
					}
,
					"id" : "obj-18",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 1084.0, 94.0, 163.0, 22.0 ],
					"saved_object_attributes" : 					{
						"client_rect" : [ 4, 79, 604, 1016 ],
						"parameter_enable" : 0,
						"parameter_mappable" : 0,
						"storage_rect" : [ 583, 69, 1034, 197 ]
					}
,
					"text" : "pattrstorage PM1 @greedy 1",
					"varname" : "PM1"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-17",
					"maxclass" : "button",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "bang" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 866.0, -5.0, 24.0, 24.0 ]
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-14",
					"maxclass" : "button",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "bang" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 786.0, -8.0, 24.0, 24.0 ]
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-12",
					"maxclass" : "button",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "bang" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 679.0, -18.0, 24.0, 24.0 ]
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-10",
					"maxclass" : "newobj",
					"numinlets" : 3,
					"numoutlets" : 1,
					"outlettype" : [ "signal" ],
					"patching_rect" : [ 864.0, 27.0, 63.0, 22.0 ],
					"text" : "MLE.hihat"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-9",
					"maxclass" : "newobj",
					"numinlets" : 3,
					"numoutlets" : 1,
					"outlettype" : [ "signal" ],
					"patching_rect" : [ 780.0, 27.0, 67.0, 22.0 ],
					"text" : "MLE.snare"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-8",
					"maxclass" : "newobj",
					"numinlets" : 3,
					"numoutlets" : 1,
					"outlettype" : [ "signal" ],
					"patching_rect" : [ 679.0, 27.0, 91.0, 22.0 ],
					"text" : "MLE.bassDrum"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-7",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 2,
					"outlettype" : [ "signal", "signal" ],
					"patching_rect" : [ 141.0, 245.0, 97.0, 22.0 ],
					"text" : "MLE.comp -10 2"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-6",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 3,
					"outlettype" : [ "", "", "" ],
					"patching_rect" : [ 141.0, -18.0, 79.0, 22.0 ],
					"text" : "MLE.midiKey"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-5",
					"maxclass" : "ezdac~",
					"numinlets" : 2,
					"numoutlets" : 0,
					"patching_rect" : [ 163.0, 765.0, 45.0, 45.0 ]
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-4",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "signal" ],
					"patching_rect" : [ 163.0, 676.0, 40.0, 22.0 ],
					"text" : "*~ 0.2"
				}

			}
, 			{
				"box" : 				{
					"bgmode" : 0,
					"border" : 0,
					"clickthrough" : 0,
					"enablehscroll" : 0,
					"enablevscroll" : 0,
					"id" : "obj-3",
					"lockeddragscroll" : 0,
					"maxclass" : "bpatcher",
					"name" : "MLE.FMsynth.maxpat",
					"numinlets" : 3,
					"numoutlets" : 2,
					"offset" : [ 0.0, 0.0 ],
					"outlettype" : [ "signal", "" ],
					"patching_rect" : [ 987.0, 255.0, 450.0, 361.0 ],
					"varname" : "MLE.FMsynth",
					"viewvisibility" : 1
				}

			}
, 			{
				"box" : 				{
					"bgmode" : 0,
					"border" : 0,
					"clickthrough" : 0,
					"enablehscroll" : 0,
					"enablevscroll" : 0,
					"id" : "obj-2",
					"lockeddragscroll" : 0,
					"maxclass" : "bpatcher",
					"name" : "MLE.moog.maxpat",
					"numinlets" : 1,
					"numoutlets" : 1,
					"offset" : [ 0.0, 0.0 ],
					"outlettype" : [ "signal" ],
					"patching_rect" : [ 133.0, 297.0, 850.0, 319.0 ],
					"varname" : "MLE.moog",
					"viewvisibility" : 1
				}

			}
, 			{
				"box" : 				{
					"bgmode" : 0,
					"border" : 0,
					"clickthrough" : 0,
					"enablehscroll" : 0,
					"enablevscroll" : 0,
					"id" : "obj-1",
					"lockeddragscroll" : 0,
					"maxclass" : "bpatcher",
					"name" : "MLE.analogueDrums.maxpat",
					"numinlets" : 1,
					"numoutlets" : 2,
					"offset" : [ 0.0, 0.0 ],
					"outlettype" : [ "signal", "signal" ],
					"patching_rect" : [ 147.0, 21.0, 487.0, 215.0 ],
					"varname" : "MLE.analogueDrums",
					"viewvisibility" : 1
				}

			}
 ],
		"lines" : [ 			{
				"patchline" : 				{
					"destination" : [ "obj-7", 0 ],
					"source" : [ "obj-1", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-4", 0 ],
					"source" : [ "obj-10", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-8", 0 ],
					"source" : [ "obj-12", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-9", 0 ],
					"source" : [ "obj-14", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-10", 0 ],
					"source" : [ "obj-17", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-4", 0 ],
					"source" : [ "obj-2", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-18", 0 ],
					"source" : [ "obj-20", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-21", 0 ],
					"source" : [ "obj-23", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-18", 0 ],
					"source" : [ "obj-26", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-33", 0 ],
					"source" : [ "obj-29", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-4", 0 ],
					"source" : [ "obj-3", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-29", 0 ],
					"source" : [ "obj-31", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-34", 1 ],
					"source" : [ "obj-33", 1 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-34", 0 ],
					"source" : [ "obj-33", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-2", 0 ],
					"source" : [ "obj-34", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-44", 0 ],
					"source" : [ "obj-35", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-35", 0 ],
					"source" : [ "obj-37", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-29", 1 ],
					"source" : [ "obj-39", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-5", 1 ],
					"order" : 0,
					"source" : [ "obj-4", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-5", 0 ],
					"order" : 1,
					"source" : [ "obj-4", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-45", 0 ],
					"source" : [ "obj-44", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-29", 0 ],
					"source" : [ "obj-45", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-46", 0 ],
					"source" : [ "obj-53", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-46", 0 ],
					"source" : [ "obj-55", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-46", 0 ],
					"source" : [ "obj-57", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-45", 0 ],
					"source" : [ "obj-58", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-3", 0 ],
					"source" : [ "obj-6", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-29", 0 ],
					"source" : [ "obj-62", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-4", 0 ],
					"source" : [ "obj-7", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-4", 0 ],
					"source" : [ "obj-8", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-4", 0 ],
					"source" : [ "obj-9", 0 ]
				}

			}
 ],
		"parameters" : 		{
			"obj-1::obj-40" : [ "tom-decay", "decay", 0 ],
			"obj-1::obj-44" : [ "trig_6", "trig_6", 0 ],
			"obj-1::obj-41" : [ "tom-hi", "hi", 0 ],
			"obj-1::obj-119" : [ "choke", "choke", 0 ],
			"obj-1::obj-42" : [ "tom-mid", "mid", 0 ],
			"obj-1::obj-46" : [ "ad-level", "level", 0 ],
			"obj-1::obj-43" : [ "tom-low", "low", 0 ],
			"obj-1::obj-17" : [ "snare-level", "level", 0 ],
			"obj-1::obj-9" : [ "kick-level", "level", 0 ],
			"obj-1::obj-19" : [ "snare-hicut", "hicut", 0 ],
			"obj-1::obj-31" : [ "clhat-decay", "cl-dec", 0 ],
			"obj-1::obj-128" : [ "trig_7[1]", "trig_7", 0 ],
			"obj-1::obj-34" : [ "trig_5", "trig_5", 0 ],
			"obj-45" : [ "live.grid", "live.grid", 0 ],
			"obj-1::obj-23" : [ "trig_3", "trig_3", 0 ],
			"obj-1::obj-129" : [ "trig_6[1]", "trig_6", 0 ],
			"obj-1::obj-20" : [ "snare-decay", "decay", 0 ],
			"obj-1::obj-120" : [ "accent", "accent", 0 ],
			"obj-1::obj-21" : [ "snare-snap", "snap", 0 ],
			"obj-1::obj-32" : [ "hat-tone", "tone", 0 ],
			"obj-1::obj-22" : [ "snare-tune", "tuning", 0 ],
			"obj-1::obj-45" : [ "trig_7", "trig_7", 0 ],
			"obj-1::obj-27" : [ "hat-level", "level", 0 ],
			"obj-1::obj-6" : [ "kick-attack", "attack", 0 ],
			"obj-1::obj-30" : [ "ophat-decay", "op-dec", 0 ],
			"obj-1::obj-5" : [ "kick-decay", "decay", 0 ],
			"obj-1::obj-4" : [ "kick-sweep", "sweep", 0 ],
			"obj-1::obj-12" : [ "trig_2", "trig_2", 0 ],
			"obj-1::obj-3" : [ "kick-tune[1]", "tuning", 0 ],
			"obj-1::obj-7" : [ "trig_1", "trig_1", 0 ],
			"obj-1::obj-33" : [ "trig_4", "trig_4", 0 ],
			"obj-1::obj-38" : [ "tom-level", "level", 0 ],
			"parameterbanks" : 			{

			}

		}
,
		"dependency_cache" : [ 			{
				"name" : "MLE.analogueDrums.maxpat",
				"bootpath" : "/Users/famle/CML/MLE/patchers/audio/drums",
				"patcherrelativepath" : "../../../../MLE/patchers/audio/drums",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "thru.maxpat",
				"bootpath" : "C74:/patchers/m4l/Pluggo for Live resources/patches",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "analog.Kick~.maxpat",
				"bootpath" : "C74:/packages/Max for Live/patchers/Max Instrument/Analogue Drums",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "analog.Snare~.maxpat",
				"bootpath" : "C74:/packages/Max for Live/patchers/Max Instrument/Analogue Drums",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "analog.Hihat~.maxpat",
				"bootpath" : "C74:/packages/Max for Live/patchers/Max Instrument/Analogue Drums",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "analog.Tom~.maxpat",
				"bootpath" : "C74:/packages/Max for Live/patchers/Max Instrument/Analogue Drums",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "MLE.moog.maxpat",
				"bootpath" : "/Users/famle/CML/MLE/patchers/audio/moog",
				"patcherrelativepath" : "../../../../MLE/patchers/audio/moog",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "MLE.moogVoice.maxpat",
				"bootpath" : "/Users/famle/CML/MLE/patchers/audio/moog",
				"patcherrelativepath" : "../../../../MLE/patchers/audio/moog",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "PM.Ladder~.maxpat",
				"bootpath" : "~/Dropbox (Personal)/_documents/MaxIH/ current/ externals/petermcculloch/Modular",
				"patcherrelativepath" : "../../../../../../ianhattwick/Dropbox (Personal)/_documents/MaxIH/ current/ externals/petermcculloch/Modular",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "MLE.bb.moogOsc.maxpat",
				"bootpath" : "/Users/famle/CML/MLE/patchers/audio/buildingBlocks",
				"patcherrelativepath" : "../../../../MLE/patchers/audio/buildingBlocks",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "MLE.bb.lfo.maxpat",
				"bootpath" : "/Users/famle/CML/MLE/patchers/audio/buildingBlocks",
				"patcherrelativepath" : "../../../../MLE/patchers/audio/buildingBlocks",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "testMoog.json",
				"bootpath" : "/Users/famle/CML/MLE/patchers/audio/moog",
				"patcherrelativepath" : "../../../../MLE/patchers/audio/moog",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "init.maxpat",
				"bootpath" : "/Users/famle/CML/MLE/patchers/utilities",
				"patcherrelativepath" : "../../../../MLE/patchers/utilities",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "MLE.polyMidi.maxpat",
				"bootpath" : "/Users/famle/CML/MLE/patchers/utilities",
				"patcherrelativepath" : "../../../../MLE/patchers/utilities",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "MLE.FMsynth.maxpat",
				"bootpath" : "/Users/famle/CML/MLE/patchers/audio/FMsynth",
				"patcherrelativepath" : "../../../../MLE/patchers/audio/FMsynth",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "MLE.fmPoly.maxpat",
				"bootpath" : "/Users/famle/CML/MLE/patchers/audio/FMsynth",
				"patcherrelativepath" : "../../../../MLE/patchers/audio/FMsynth",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "MLE.pattrNamer.maxpat",
				"bootpath" : "/Users/famle/CML/MLE/patchers/sandbox",
				"patcherrelativepath" : "../../../../MLE/patchers/sandbox",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "MLE.midiKey.maxpat",
				"bootpath" : "/Users/famle/CML/MLE/patchers/controllers",
				"patcherrelativepath" : "../../../../MLE/patchers/controllers",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "MLE.comp.maxpat",
				"bootpath" : "/Users/famle/CML/MLE/patchers/sandbox/Carina/MLE FX library",
				"patcherrelativepath" : "../../../../MLE/patchers/sandbox/Carina/MLE FX library",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "MLE.bassDrum.maxpat",
				"bootpath" : "/Users/famle/CML/MLE/patchers/audio/drums",
				"patcherrelativepath" : "../../../../MLE/patchers/audio/drums",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "MLE.snare.maxpat",
				"bootpath" : "/Users/famle/CML/MLE/patchers/audio/drums",
				"patcherrelativepath" : "../../../../MLE/patchers/audio/drums",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "MLE.hihat.maxpat",
				"bootpath" : "/Users/famle/CML/MLE/patchers/audio/drums",
				"patcherrelativepath" : "../../../../MLE/patchers/audio/drums",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "MLE.scale.maxpat",
				"bootpath" : "/Users/famle/CML/MLE/patchers/controllers",
				"patcherrelativepath" : "../../../../MLE/patchers/controllers",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "initS.maxpat",
				"bootpath" : "/Users/famle/CML/MLE/patchers/utilities",
				"patcherrelativepath" : "../../../../MLE/patchers/utilities",
				"type" : "JSON",
				"implicit" : 1
			}
 ],
		"autosave" : 0
	}

}
