class BasePythonMethodProcessor:
    @rx.event
    def update_current_answers(self, current_answers: Dict[str, Any]) -> bool:
        """
        Updates !!! current !! answers based on data from API!!!!!@@@@@@@22222234343434 ###
        """
        logger.debug(f'Updating current answers with: {current_answers} !!')
        self.current_answers = current_answers