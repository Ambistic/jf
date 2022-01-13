class Profiler:
    def __enter__(self):
        import cProfile

        self.pr = cProfile.Profile()
        self.pr.enable()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        import pstats, io
        self.pr.disable()
        s = io.StringIO()
        sortby = "cumulative"
        ps = pstats.Stats(self.pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())