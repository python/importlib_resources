import hydra

@hydra.main(config_path='.', config_name='run')
def test(cfg):
    pass

if __name__ == "__main__":
    test()