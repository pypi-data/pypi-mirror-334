"""
AuxKnow Search: A simple Search Engine to enhance the capabilities of AuxKnow.

This module provides a Search Engine to help build custom search capabilities for AuxKnow.

Author: Aditya Patange (AdiPat)
Copyright (c) 2025 The Hackers Playbook
License: AGPLv3
"""

from langchain_community.tools import DuckDuckGoSearchResults
import traceback
from pydantic import BaseModel
from .printer import Printer
from typing import Union
from .constants import Constants


class AuxKnowSearchItem(BaseModel):
    """
    AuxKnowSearchResults: A simple Search Engine to enhance the capabilities of AuxKnow.
    """

    title: str
    content: str
    url: str


class AuxKnowSearchResults(BaseModel):
    """
    AuxKnowSearchResults: A simple Search Engine to enhance the capabilities of AuxKnow.
    """

    results: list[AuxKnowSearchItem]


class AuxKnowSearch:
    """
    AuxKnowSearch: A simple Search Engine to enhance the capabilities of AuxKnow.
    """

    def __init__(self, verbose=Constants.DEFAULT_VERBOSE_ENABLED):
        """
        Initializes the AuxKnow Search Engine.

        Args:
            verbose (bool, optional): Whether to print verbose messages. Defaults to DEFAULT_AUXKNOW_SEARCH_VERBOSE.
        """
        self.verbose = verbose
        Printer.verbose_logger(
            self.verbose,
            Printer.print_blue_message,
            "🔦 Initializing the AuxKnow Search Engine...",
        )
        self.search = DuckDuckGoSearchResults(output_format="list")
        Printer.verbose_logger(
            self.verbose,
            Printer.print_green_message,
            "🔦 Initialized the AuxKnow Search Engine! 🚀",
        )

    def query(self, query: str) -> tuple[Union[AuxKnowSearchResults, None], str]:
        """
        Queries the AuxKnow Search Engine.

        Args:
            query (str): The query to search for.

        Returns:
            tuple[Union[AuxKnowSearchResults, None], str]: The search results and the error message.
        """
        try:
            Printer.verbose_logger(
                self.verbose,
                Printer.print_yellow_message,
                f"🔍 Searching for: '{query}'",
            )
            results = self.search.invoke(query)
            results = []
            for result in results:
                results.append(
                    AuxKnowSearchItem(
                        title=result["title"],
                        content=result["snippet"],
                        url=result["url"],
                    )
                )
            Printer.verbose_logger(
                self.verbose,
                Printer.print_green_message,
                f"✨ Found {len(results)} results",
            )
            return AuxKnowSearchResults(results=results), ""
        except Exception as e:
            error_msg = f"Error while querying the AuxKnow Search Engine: {e}"
            Printer.verbose_logger(self.verbose, Printer.print_red_message, error_msg)
            if self.verbose:
                traceback.print_exc()
            return None, str(e)
