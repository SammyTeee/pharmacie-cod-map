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
	zm_usermap::main();
	
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
	zm_zonemgr::add_adjacent_zone( "v58_route_town_0_0", "v58_route_town_0_1", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_town_0_1", "v58_route_town_1_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_town_1_0", "v58_route_town_1_1", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_town_1_1", "v58_route_town_2_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_town_2_0", "v58_route_town_2_1", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_town_2_1", "v58_route_town_3_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_town_3_0", "v58_route_town_3_1", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_town_3_1", "v58_route_town_4_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_town_4_0", "v58_route_town_4_1", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_town_4_1", "v58_route_town_5_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_town_5_0", "v58_route_town_6_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_town_6_0", "v58_route_town_7_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "street_zone", "v58_route_town_0_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_main_0_0", "v58_route_main_1_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_main_1_0", "v58_route_main_2_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_main_2_0", "v58_route_main_3_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_main_3_0", "v58_route_main_3_1", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_main_3_1", "v58_route_main_4_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_main_4_0", "v58_route_main_4_1", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_main_4_1", "v58_route_main_5_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_main_5_0", "v58_route_main_5_1", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_main_5_1", "v58_route_main_6_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_main_6_0", "v58_route_main_6_1", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_main_6_1", "v58_route_main_6_2", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_main_6_2", "v58_route_main_7_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_main_7_0", "v58_route_main_7_1", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_main_7_1", "v58_route_main_8_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_main_8_0", "v58_route_main_9_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_main_9_0", "v58_route_main_10_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_main_10_0", "v58_route_main_11_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_main_11_0", "v58_route_main_12_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_main_12_0", "v58_route_main_13_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_main_13_0", "v58_route_main_14_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_main_14_0", "v58_route_main_15_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_main_15_0", "v58_route_main_16_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_main_16_0", "v58_route_main_17_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_main_17_0", "v58_route_main_18_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_main_18_0", "v58_route_main_19_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_main_19_0", "v58_route_main_19_1", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_main_19_1", "v58_route_main_20_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_town_7_0", "v58_route_main_0_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_holmdale_0_0", "v58_route_holmdale_1_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_holmdale_1_0", "v58_route_holmdale_2_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_holmdale_2_0", "v58_route_holmdale_3_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_holmdale_3_0", "v58_route_holmdale_4_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_holmdale_4_0", "v58_route_holmdale_4_1", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_main_15_0", "v58_route_holmdale_0_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_station_access_0_0", "v58_route_station_access_1_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_station_access_1_0", "v58_route_station_access_2_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_station_access_2_0", "v58_route_station_access_3_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_station_access_3_0", "v58_route_station_access_4_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_station_access_4_0", "v58_route_station_access_5_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_main_17_0", "v58_route_station_access_0_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_barkby_0_0", "v58_route_barkby_1_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_barkby_1_0", "v58_route_barkby_2_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_barkby_2_0", "v58_route_barkby_3_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_barkby_3_0", "v58_route_barkby_4_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_barkby_4_0", "v58_route_barkby_5_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_barkby_5_0", "v58_route_barkby_6_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "v58_route_barkby_6_0", "v58_route_barkby_7_0", "always_on" );
	zm_zonemgr::add_adjacent_zone( "street_zone", "v58_route_barkby_0_0", "always_on" );



























































































































































































	zm_zonemgr::add_adjacent_zone( "start_zone", "street_zone", "pt58_street_open" );
	zm_zonemgr::add_adjacent_zone( "start_zone", "upstairs_zone", "pt58_stairs_open" );
	zm_zonemgr::add_adjacent_zone( "street_zone", "crossing_zone", "pt58_crossing_open" );
}	

function custom_add_weapons()
{
	zm_weapons::load_weapon_spec_from_table("gamedata/weapons/zm/zm_levelcommon_weapons.csv", 1);
	// Sam requested free wall weapons and ordinary ammo for this test.
	foreach (weapon, spec in level.zombie_weapons)
	{
		level.zombie_weapons[weapon].cost = 0;
		level.zombie_weapons[weapon].ammo_cost = 0;
	}
}

