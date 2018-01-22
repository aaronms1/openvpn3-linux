//  OpenVPN 3 Linux client -- Next generation OpenVPN client
//
//  Copyright (C) 2018         OpenVPN, Inc. <sales@openvpn.net>
//  Copyright (C) 2018         David Sommerseth <davids@openvpn.net>
//
//  This program is free software: you can redistribute it and/or modify
//  it under the terms of the GNU Affero General Public License as
//  published by the Free Software Foundation, version 3 of the
//  License.
//
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU Affero General Public License for more details.
//
//  You should have received a copy of the GNU Affero General Public License
//  along with this program.  If not, see <https://www.gnu.org/licenses/>.
//

/**
 * @file   lookup-tests.cpp
 *
 * @brief  Simple unit tests which checks lookup_uid(), lookup_username() and
 *         isanum_string()
 */

#include <iostream>

#include "common/utils.hpp"
#include "ovpn3cli/lookup.hpp"

int main(int argc, char **argv)
{
    if (1 == argc)
    {
        std::cout << ">> Username -> UID lookups" << std::endl;
        uid_t root = lookup_uid("root");
        uid_t nobody = lookup_uid("nobody");
        uid_t invalid = lookup_uid("nonexiting_user");

        std::cout << "     root uid: " << root << std::endl;
        std::cout << "   nobody uid: " << nobody << std::endl;
        std::cout << "      invalid: "
                  << (-1 == invalid ? "(correct, not found)" : "**ERROR**")
                  << std::endl;
        std::cout << std::endl;

        std::cout << ">> UID -> username lookups" << std::endl;
        std::string root_username = lookup_username(root);
        std::string nobody_username = lookup_username(nobody);
        std::cout << "   Lookup UID " << root << ": username "
                  << root_username << std::endl;
        std::cout << "   Lookup UID " << nobody << ": username "
                  << nobody_username << std::endl;
        std::cout << std::endl;

        if (("root" == root_username)
            && ("nobody" == nobody_username)
            && (-1 == invalid))
        {
            std::cout << "** Result: All tests passed" << std::endl;
            return 0;
        }
        std::cout << "** Result: FAIL" << std::endl;
        return 1;
    }
    else {
        if (isanum_string(argv[1]))
        {
            std::string username = lookup_username(std::stoi(argv[1]));
            std::cout << "UID " << argv[1]
                      << " maps to '" << username << "'" << std::endl;
        }
        else
        {
            uid_t uid = lookup_uid(argv[1]);
            if (-1 != uid) {
                std::cout << "Username '" << argv[1] << "'"
                          << " maps to UID " << std::to_string(uid) << std::endl;
            }
            else {
                std::cout << "Username '" << argv[1] << "' not found" << std::endl;
            }
        }
    }
    return 0;
}
