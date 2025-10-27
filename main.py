import utils.argparser
import utils.application

def main():
    args = utils.argparser.initialzie_argparser()
    app = utils.application.Application(
        path=args.path,
        colored=args.colored,
        output_path=args.output_path,
        threshold=args.threshold,
        output_type=args.output_type,
    )
    app.run()
    

if __name__ == "__main__":
    main()
