from abc import ABC, abstractmethod

class BaseExtractor(ABC):
    @abstractmethod
    def extract(self, text: str) -> dict:
        """
        Extract structured attributes from a product description text.
        
        Args:
            text (str): Unstructured fashion/apparel product description.
            
        Returns:
            dict: A dictionary containing the 8 canonical fields:
                  - silhouette (str or None)
                  - fabric (str or None)
                  - neckline (str or None)
                  - sleeve (str or None)
                  - length (str or None)
                  - embellishment (str or None)
                  - color (list of str)
                  - category (str or None)
                  And optionally metadata fields like 'confidence' or 'matched_terms'.
        """
        pass
