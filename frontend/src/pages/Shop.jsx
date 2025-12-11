import '../App.css';

export default function Shop() {
  return (
    <section className="shop">
        <h2>Our Shop</h2>
        <p className="shop-intro">
            Explore Inkspire’s exclusive range of tattoo supplies, aftercare essentials, and merchandise.
        </p>

        <div className="shop-grid">
            {/* Product 1 */}
            <div className="product">
                <img src="images/Ink.jpg" alt="Tattoo Ink Set" />
                <h3>Tattoo Ink Set</h3>
                <p>High-quality professional-grade ink for vibrant and lasting colors.</p>
                <span className="price">$95</span>
                <button className="btn">Buy Now</button>
            </div>

            {/* Product 2 */}
            <div className="product">
                <img src="images/tattoobalm.jpg" alt="Tattoo Aftercare Cream" />
                <h3>Aftercare Cream</h3>
                <p>Keep your tattoos fresh and vibrant with our natural healing balm.</p>
                <span className="price">$15</span>
                <button className="btn">Buy Now</button>
            </div>

            {/* Product 3 */}
            <div className="product">
                <img src="images/tshirt.jpg" alt="Inkspire T-shirt" />
                <h3>Inkspire T-Shirt</h3>
                <p>Represent your passion for art with our comfortable studio apparel.</p>
                <span className="price">$25</span>
                <button className="btn">Buy Now</button>
            </div>

            {/* Product 4 */}
            <div className="product">
                <img src="images/tattooneedle.jpg" alt="Professional Tattoo Needles" />
                <h3>Tattoo Needles</h3>
                <p>Precision needles for clean lines and smooth shading.</p>
                <span className="price">$35</span>
                <button className="btn">Buy Now</button>
            </div>

        </div>
    </section>
  );
}