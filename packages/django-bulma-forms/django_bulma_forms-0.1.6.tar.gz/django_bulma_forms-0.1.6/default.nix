{
  sources ? import ./npins,
  pkgs ? import sources.nixpkgs { },
}:

let
  check = (import sources.git-hooks).run {
    src = ./.;

    hooks = {
      # Python hooks
      ruff.enable = true;
      black.enable = true;
      isort.enable = true;

      # Nix Hooks
      statix.enable = true;
      deadnix.enable = true;

      # Misc Hooks
      commitizen.enable = true;
    };
  };

  deploy-pypi = pkgs.writeShellApplication {
    name = "deploy-pypi";

    runtimeInputs = [
      (pkgs.python3.withPackages (ps: [
        ps.setuptools
        ps.build
        ps.twine
      ]))
    ];

    text = ''
      # Clean the repository
      rm -rf dist

      python -m build
      twine upload dist/*
    '';
  };
in

{
  devShell = pkgs.mkShell {
    name = "dj-bulma-forms.dev";

    packages = [
      # Python dependencies
      (pkgs.python3.withPackages (ps: [
        ps.django
        ps.django-types
      ]))
    ] ++ check.enabledPackages;

    shellHook = ''
      ${check.shellHook}
    '';
  };

  publishShell = pkgs.mkShell {
    name = "dj-bulma-forms.publish";

    packages = [ deploy-pypi ];
  };
}
