#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2024 Tom Noble.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#    * Neither the name of the copyright holder nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

# Author: Tom Noble

import sys
import argparse
import logging
from typing import List, Tuple
from pathlib import Path


DISCLAIMER = """
/*********************************************************************
 * All MoveIt 2 headers have been updated to use the .hpp extension.
 *
 * .h headers are now autogenerated via {},
 * and will import the corresponding .hpp with a deprecation warning.
 *
 * imports via .h files may be removed in future releases, so please
 * modify your imports to use the corresponding .hpp imports.
 *
 * See https://github.com/moveit/moveit2/pull/3113 for extra details.
 *********************************************************************/
"""


class NoIncludeGuard(Exception):
    ERROR = "No include guard found in {}.hpp. Unable to generate pretext."

    def __init__(self, file: Path):
        super().__init__(self.ERROR.format(file))


class NoIncludeDirectory(Exception):
    ERROR = "No include directory found for {}.hpp. Unable to generate relative .hpp include"

    def __init__(self, file: Path):
        super().__init__(self.ERROR.format(file))


class HppFile:
    def __init__(self, path: Path):
        self.path = path
        self.guard = "#pragma once"
        self.pretext = self.pretext()
        self.include = self.include()

    def drop_data_after(self, data: str, match: str):
        return data[: data.find(match) + len(match)]

    def read(self) -> str:
        data = open(self.path, "r").read()
        contains_guard = self.guard in data
        if not contains_guard:
            raise NoIncludeGuard(self.path)
        return data

    def pretext(self) -> str:
        data = self.read()
        return self.drop_data_after(data, self.guard)

    def include(self) -> str:
        ends_with_include = lambda p: str(p).endswith("include")
        include_paths = [p for p in self.path.parents if ends_with_include(p)]
        if not include_paths:
            raise NoIncludeDirectory(self.path)
        relative_import = self.path.relative_to(include_paths[0])
        return f"#include <{relative_import}>"


class DeprecatedHeader:
    def __init__(self, hpp: HppFile):
        self.hpp = hpp
        self.path = hpp.path.with_suffix(".h")
        self.warn = '#pragma message(".h header is obsolete. Please use the .hpp header instead.")'
        self.contents = self.contents()

    def contents(self) -> str:
        disclaimer = DISCLAIMER.format(Path(__file__).name).rstrip("\n")
        items = [disclaimer, self.hpp.pretext, self.warn, self.hpp.include]
        return "\n".join(items) + "\n"


class HeaderSummary:
    def __init__(self, n_processed_hpps: int, bad_hpps: List[str]):
        self.n_processed_hpps = n_processed_hpps
        self.bad_hpps = bad_hpps

    def were_all_hpps_processed(self) -> bool:
        return len(self.bad_hpps) == 0

    def __repr__(self) -> str:
        summary = f"Can generate {self.n_processed_hpps} .h files."
        if self.bad_hpps:
            summary += f" Cannot generate {len(self.bad_hpps)} .h files:\n\n"
            summary += "\n".join([f"❌ {hpp}" for hpp in self.bad_hpps])
            summary += "\n"
        return summary


class DeprecatedHeaderGenerator:
    def __init__(self, hpp_paths: List[str]):
        self.hpp_paths = hpp_paths
        self.processed_hpps = []
        self.bad_hpps = []

    def __process_hpp(self, hpp: str) -> None:
        try:
            self.processed_hpps.append(HppFile(hpp))
        except (NoIncludeDirectory, NoIncludeGuard) as e:
            self.bad_hpps.append(str(hpp))

    def process_all_hpps(self) -> HeaderSummary:
        print(f"\nProcessing {len(self.hpp_paths)} .hpp files...")
        _ = [self.__process_hpp(hpp) for hpp in self.hpp_paths]
        return HeaderSummary(len(self.processed_hpps), self.bad_hpps)

    def create_h_files(self) -> None:
        print(f"Proceeding to generate {len(self.processed_hpps)} .h files...")
        h_files = [DeprecatedHeader(hpp) for hpp in self.processed_hpps]
        _ = [open(h.path, "w").write(h.contents) for h in h_files]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # TODO: Add argument for skipping private headers
    parser.add_argument("--apply", action="store_true", help="Generates the .h files")
    args = parser.parse_args()
    generator = DeprecatedHeaderGenerator(list(Path.cwd().rglob("*.hpp")))
    summary = generator.process_all_hpps()
    print(summary)
    if args.apply and not summary.were_all_hpps_processed():
        args.apply = input("Continue? (y/n): ").lower() == "y"
    if args.apply:
        generator.create_h_files()
    else:
        print("Skipping file generation...")
    print("Done.\n")