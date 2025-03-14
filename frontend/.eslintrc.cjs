/**
 * This is intended to be a basic starting point for linting in your app.
 * It relies on recommended configs out of the box for simplicity, but you can
 * and should modify this configuration to best suit your team's needs.
 */

/** @type {import('eslint').Linter.Config} */
module.exports = {
  extends: "@remix-run/eslint-config",
  rules: {
    "@typescript-eslint/ban-ts-comment": "off",
    "no-unused-vars": "off"
  },
};
