
/*********************************************************************
 * All MoveIt 2 headers have been updated to use the .hpp extension.
 *
 * .h headers are now autogenerated via create_deprecated_headers.py,
 * and will import the corresponding .hpp with a deprecation warning.
 *
 * imports via .h files may be removed in future releases, so please
 * modify your imports to use the corresponding .hpp imports.
 *
 * See https://github.com/moveit/moveit2/pull/3113 for extra details.
 *********************************************************************/
// Copyright  (C)  2007  Ruben Smits <ruben dot smits at mech dot kuleuven dot be>

// Version: 1.0
// Author: Ruben Smits <ruben dot smits at mech dot kuleuven dot be>
// Maintainer: Ruben Smits <ruben dot smits at mech dot kuleuven dot be>
// URL: http://www.orocos.org/kdl

// This library is free software; you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public
// License as published by the Free Software Foundation; either
// version 2.1 of the License, or (at your option) any later version.

// This library is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
// Lesser General Public License for more details.

// You should have received a copy of the GNU Lesser General Public
// License along with this library; if not, write to the Free Software
// Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

// Modified to account for "mimic" joints, i.e. joints whose motion has a
// linear relationship to that of another joint.
// Copyright  (C)  2013  Sachin Chitta, Willow Garage

#pragma once
#pragma message(".h header is obsolete. Please use the .hpp header instead.")
#include <moveit/kdl_kinematics_plugin/chainiksolver_vel_mimic_svd.hpp>
