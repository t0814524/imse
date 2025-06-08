const webpack = require('webpack')
const path = require('path')
// const NodePolyfillPlugin = require("node-polyfill-webpack-plugin")
// const CopyPlugin = require('copy-webpack-plugin');
const TerserPlugin = require('terser-webpack-plugin') //todo: minify that shit, but production doesnt seem to work

const config = {
    entry: {
        mylib: path.resolve(__dirname, 'ts/init.ts')
    },
    module: {
        rules: [
            {
                test: /\.ts$/,
                exclude: [/node_modules/],
                loader: 'ts-loader'
            }
        ]
    },
    resolve: {
        extensions: ['.ts', '.js'],
        // alias: aliasConfig
    },
    output: {
        publicPath: "static",
        path: path.resolve(__dirname, 'server/static/js'),
        chunkFilename: 'bundle.js',
        filename: 'bundle.js'
    },
    mode: 'development',
    // watch: true,
    plugins: [

        // new NodePolyfillPlugin({
        //     excludeAliases: ["console"]
        // }),

    ],
    devtool: 'source-map',
    optimization: {
        minimizer: [
            new TerserPlugin({
                minify: TerserPlugin.terserMinify,
                terserOptions: {
                    compress: {
                        drop_console: true
                    }
                }
            })
        ]
    },
    // production build does not work rn. I think it is because of the ts errors. if i remove everything from the entry file it works
    // bail: false,
    // optimization: {
    // minimize: true
    // splitChunks: {
    //     cacheGroups: {
    //         vendors: {
    //             priority: -10,
    //             test: /[\\/]node_modules[\\/]/
    //         }
    //     },

    //     chunks: 'async',
    //     minChunks: 1,
    //     minSize: 30000,
    //     name: true
    // }
    // }
}

module.exports = config