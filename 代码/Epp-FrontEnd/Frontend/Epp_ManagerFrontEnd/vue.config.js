let path = require("path");
const webpack = require("webpack");
const ThemeColorReplacer = require("webpack-theme-color-replacer");
const { getThemeColors, modifyVars } = require("./src/utils/themeUtil");
const { resolveCss } = require("./src/utils/theme-color-replacer-extend");
const CompressionWebpackPlugin = require("compression-webpack-plugin");

const productionGzipExtensions = ["js", "css"];
const isProd = process.env.NODE_ENV === "production";

const assetsCDN = {
  // webpack build externals
  externals: {
    vue: "Vue",
    "vue-router": "VueRouter",
    vuex: "Vuex",
    axios: "axios",
    nprogress: "NProgress",
    clipboard: "ClipboardJS",
    "@antv/data-set": "DataSet",
    "js-cookie": "Cookies",
  },
  css: [],
  js: [
    "//cdnjs.cloudflare.com/ajax/libs/vue/2.6.11/vue.min.js",
    "//cdnjs.cloudflare.com/ajax/libs/vue-router/3.4.0/vue-router.min.js",
    "//cdnjs.cloudflare.com/ajax/libs/vuex/3.5.1/vuex.min.js",
    "//cdnjs.cloudflare.com/ajax/libs/axios/0.19.2/axios.min.js",
    "//cdnjs.cloudflare.com/ajax/libs/nprogress/0.2.0/nprogress.min.js",
    "//cdnjs.cloudflare.com/ajax/libs/clipboard.js/2.0.6/clipboard.min.js",
    "//gw.alipayobjects.com/os/antv/pkg/_antv.data-set-0.11.1/dist/data-set.js",
    "//cdnjs.cloudflare.com/ajax/libs/js-cookie/2.2.1/js.cookie.min.js",
  ],
};

module.exports = {
  devServer: {
    proxy: {
      "/api": {
        // target:"http://127.0.0.1:8000",
        target:"http://116.63.14.146:8000",
        // target:"http://122.9.14.73:8000/",
        changeOrigin: true,
      },
    },
    host: "0.0.0.0",
    port: 10516,
    disableHostCheck: true,
  },
  pluginOptions: {
    "style-resources-loader": {
      preProcessor: "less",
      patterns: [path.resolve(__dirname, "./src/theme/theme.less")],
    },
  },
  configureWebpack: (config) => {
    config.entry.app = ["babel-polyfill", "whatwg-fetch", "./src/main.js"];
    config.performance = {
      hints: false,
    };
    config.plugins.push(
      new ThemeColorReplacer({
        fileName: "css/theme-colors-[contenthash:8].css",
        matchColors: getThemeColors(),
        injectCss: true,
        resolveCss,
      })
    );
    // Ignore all locale files of moment.js
    config.plugins.push(new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/));
    // 生产环境下将资源压缩成gzip格式
    if (isProd) {
      // add `CompressionWebpack` plugin to webpack plugins
      config.plugins.push(
        new CompressionWebpackPlugin({
          algorithm: "gzip",
          test: new RegExp("\\.(" + productionGzipExtensions.join("|") + ")$"),
          threshold: 10240,
          minRatio: 0.8,
        })
      );
    }
    // if prod, add externals
    if (isProd) {
      config.externals = assetsCDN.externals;
    }
  },
  chainWebpack: (config) => {
    // 生产环境下关闭css压缩的 colormin 项，因为此项优化与主题色替换功能冲突
    if (isProd) {
      config.plugin("optimize-css").tap((args) => {
        args[0].cssnanoOptions.preset[1].colormin = false;
        return args;
      });
    }
    // 生产环境下使用CDN
    if (isProd) {
      config.plugin("html").tap((args) => {
        args[0].cdn = assetsCDN;
        return args;
      });
    }
  },
  css: {
    loaderOptions: {
      less: {
        lessOptions: {
          modifyVars: modifyVars(),
          javascriptEnabled: true,
        },
      },
    },
  },
  publicPath: process.env.VUE_APP_PUBLIC_PATH,
  outputDir: "dist",
  assetsDir: "static",
  productionSourceMap: false,
};
