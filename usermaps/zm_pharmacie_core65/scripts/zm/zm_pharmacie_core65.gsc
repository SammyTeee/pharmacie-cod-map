#using scripts\codescripts\struct;

#using scripts\shared\array_shared;
#using scripts\shared\callbacks_shared;
#using scripts\shared\clientfield_shared;
#using scripts\shared\compass;
#using scripts\shared\exploder_shared;
#using scripts\shared\flag_shared;
#using scripts\shared\laststand_shared;
#using scripts\shared\math_shared;
#using scripts\shared\scene_shared;
#using scripts\shared\util_shared;

#insert scripts\shared\shared.gsh;
#insert scripts\shared\version.gsh;

#insert scripts\zm\_zm_utility.gsh;

#using scripts\zm\_load;
#using scripts\zm\_zm;
#using scripts\zm\_zm_audio;
#using scripts\zm\_zm_powerups;
#using scripts\zm\_zm_utility;
#using scripts\zm\_zm_weapons;
#using scripts\zm\_zm_zonemgr;

#using scripts\shared\ai\zombie_utility;

//Perks
#using scripts\zm\_zm_pack_a_punch;
#using scripts\zm\_zm_pack_a_punch_util;
#using scripts\zm\_zm_perk_additionalprimaryweapon;
#using scripts\zm\_zm_perk_doubletap2;
#using scripts\zm\_zm_perk_deadshot;
#using scripts\zm\_zm_perk_juggernaut;
#using scripts\zm\_zm_perk_quick_revive;
#using scripts\zm\_zm_perk_sleight_of_hand;
#using scripts\zm\_zm_perk_staminup;

//Powerups
#using scripts\zm\_zm_powerup_double_points;
#using scripts\zm\_zm_powerup_carpenter;
#using scripts\zm\_zm_powerup_fire_sale;
#using scripts\zm\_zm_powerup_free_perk;
#using scripts\zm\_zm_powerup_full_ammo;
#using scripts\zm\_zm_powerup_insta_kill;
#using scripts\zm\_zm_powerup_nuke;
//#using scripts\zm\_zm_powerup_weapon_minigun;

//Traps
#using scripts\zm\_zm_trap_electric;

#using scripts\zm\zm_usermap;

//*****************************************************************************
// MAIN
//*****************************************************************************

function main()
{
	level.round_prestart_func = &core65_first_round_prestart;
	zm_usermap::main();
	level thread core65_ground_diagnostics();

	level._zombie_custom_add_weapons =&custom_add_weapons;

	//Setup the levels Zombie Zone Volumes
	level.zones = [];
	level.zone_manager_init_func =&usermap_test_zone_init;
	init_zones[0] = "start_zone";
	level thread zm_zonemgr::manage_zones( init_zones );

	level.pathdist_type = PATHDIST_ORIGINAL;
}

function usermap_test_zone_init()
{
	level flag::init( "always_on" );
	level flag::set( "always_on" );
	zm_zonemgr::add_adjacent_zone( "start_zone", "street_zone", "pt18_street_open" );
	zm_zonemgr::add_adjacent_zone( "start_zone", "upstairs_zone", "pt18_stairs_open" );
	zm_zonemgr::add_adjacent_zone( "street_zone", "crossing_zone", "pt18_crossing_open" );
}

function custom_add_weapons()
{
	zm_weapons::load_weapon_spec_from_table("gamedata/weapons/zm/zm_levelcommon_weapons.csv", 1);
}

function core65_first_round_prestart()
{
	if (!IsDefined(level.core65_prep_done))
	{
		level.core65_prep_done = true;
		IPrintLnBold("Prepare: first wave in 60 seconds");
		/# PrintLn("CORE65_PREPARATION_BEGIN seconds=60"); #/
		wait(4);
		IPrintLnBold("Bartender: You need to get down to Taraj for a Chicken Jalfrezi.");
		/# PrintLn("CORE65_STORY_INTRO taraj_jalfrezi"); #/
		wait(7);
		IPrintLnBold("Bartender: First, keep this pub standing. We will sort the road out after.");
		wait(49);
		/# PrintLn("CORE65_PREPARATION_COMPLETE"); #/
	}
	else
	{
		wait(2);
	}
}

function core65_ground_diagnostics()
{
	level endon("end_game");
	wait(4);
	points = [];
	points[0] = (62.204724, -338.582677, 0.000000);
	points[1] = (62.204724, -354.330709, 0.000000);
	points[2] = (62.204724, -370.078740, 0.000000);
	points[3] = (62.204724, -385.826772, 0.000000);
	points[4] = (62.204724, -401.574803, 0.000000);
	points[5] = (62.204724, -417.322835, 0.000000);
	points[6] = (62.204724, -433.070866, 0.000000);
	points[7] = (62.204724, -472.440945, 0.000000);
	points[8] = (62.204724, -531.496063, 0.000000);
	points[9] = (78.740157, -338.582677, 0.000000);
	points[10] = (78.740157, -354.330709, 0.000000);
	points[11] = (78.740157, -370.078740, 0.000000);
	points[12] = (78.740157, -385.826772, 0.000000);
	points[13] = (78.740157, -401.574803, 0.000000);
	points[14] = (78.740157, -417.322835, 0.000000);
	points[15] = (78.740157, -433.070866, 0.000000);
	points[16] = (78.740157, -472.440945, 0.000000);
	points[17] = (78.740157, -531.496063, 0.000000);
	points[18] = (95.275591, -338.582677, 0.000000);
	points[19] = (95.275591, -354.330709, 0.000000);
	points[20] = (95.275591, -370.078740, 0.000000);
	points[21] = (95.275591, -385.826772, 0.000000);
	points[22] = (95.275591, -401.574803, 0.000000);
	points[23] = (95.275591, -417.322835, 0.000000);
	points[24] = (95.275591, -433.070866, 0.000000);
	points[25] = (95.275591, -472.440945, 0.000000);
	points[26] = (95.275591, -531.496063, 0.000000);
	missing = 0;
	foreach (p in points)
	{
		trace = BulletTrace(p + (0,0,8), p - (0,0,28), false, undefined);
		if (trace["fraction"] >= 1)
		{
			missing++;
			/# PrintLn("CORE65_GROUND_MISS " + p); #/
		}
		wait(.01);
	}
	/# PrintLn("CORE65_GROUND_RESULT points=" + points.size + " missing=" + missing); #/
}
