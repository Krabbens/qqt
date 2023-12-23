'''class for managing the engine'''

class qqtEngineManager:
    _engine = None

    @classmethod
    def get_engine(cls):
        return cls._engine
    
    @classmethod
    def set_engine(cls, engine):
        cls._engine = engine