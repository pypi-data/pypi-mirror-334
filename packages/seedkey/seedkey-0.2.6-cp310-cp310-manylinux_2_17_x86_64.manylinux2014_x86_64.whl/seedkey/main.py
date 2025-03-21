import argparse

from . import _core


def main():
    parser = argparse.ArgumentParser(
        description="SeedKey - the Activation Tool of SeedMath"
    )

    # 添加产品选择选项组
    product_group = parser.add_mutually_exclusive_group(required=True)
    product_group.add_argument(
        "--seedmip", action="store_true", help="Activate the SeedMIP solver"
    )
    product_group.add_argument(
        "--seedsat", action="store_true", help="Activate the SeedSAT solver"
    )
    product_group.add_argument(
        "--seedsmt", action="store_true", help="Activate the SeedSMT solver"
    )
    product_group.add_argument(
        "--seedkcompiler", action="store_true", help="Activate the SeedKCompiler solver"
    )

    # 添加激活码参数
    parser.add_argument("activation_code", type=str, help="Activation code")

    args = parser.parse_args()

    # 确定要激活的产品
    if args.seedmip:
        product = "seedmip"
    elif args.seedsat:
        product = "seedsat"
    elif args.seedsmt:
        product = "seedsmt"
    elif args.seedkcompiler:
        product = "seedkcompiler"

    _core.activate(product, args.activation_code)


if __name__ == "__main__":
    import sys

    sys.exit(main())
